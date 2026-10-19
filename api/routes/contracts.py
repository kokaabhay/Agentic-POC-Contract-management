
import re
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from src.app.config import settings
from src.app.services.blob_storage import (
    blob_exists,
    download_bytes,
    list_blob_names,
    read_json,
    save_json,
    upload_bytes,
)
from src.app.services.doc_processor import extract_document


router = APIRouter(
    prefix="/contracts",
    tags=["Contract Management"],
)


def normalize_batch_name(name: str) -> str:
    """Convert a user-provided batch name into a safe path segment."""

    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", name.strip())
    slug = slug.strip("-_").lower()

    if not slug:
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid batch name.",
        )

    return slug[:60]


def get_batch_prefix(batch_id: str) -> str:
    return f"{settings.contract_documents_prefix}/{batch_id}"


@router.post("/upload", status_code=201)
async def upload_contract_batch(
    batch_name: str = Form(...),
    files: list[UploadFile] = File(...),
):
    """
    Upload multiple contract documents as one batch.

    Each batch gets a unique folder-like prefix in Blob Storage.
    """

    if not batch_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Batch name cannot be empty.",
        )

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Upload at least one contract document.",
        )

    if len(files) > settings.max_files_per_batch:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Maximum files per batch: "
                f"{settings.max_files_per_batch}."
            ),
        )

    # Validate all filenames before uploading anything.
    prepared_files = []
    seen_names = set()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024

    for file in files:
        filename = (file.filename or "").replace("\\", "/").split("/")[-1]

        if not filename or filename in {".", ".."}:
            raise HTTPException(
                status_code=400,
                detail="A file has an invalid filename.",
            )

        extension = Path(filename).suffix.lower()

        if extension not in settings.allowed_extension_set:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported file type for '{filename}'. "
                    f"Allowed types: "
                    f"{sorted(settings.allowed_extension_set)}."
                ),
            )

        if filename.lower() in seen_names:
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate filename in batch: {filename}",
            )

        seen_names.add(filename.lower())

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail=f"File '{filename}' is empty.",
            )

        if len(content) > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=(
                    f"File '{filename}' exceeds "
                    f"{settings.max_upload_size_mb} MB."
                ),
            )

        prepared_files.append(
            {
                "filename": filename,
                "content": content,
                "content_type": (
                    file.content_type or "application/octet-stream"
                ),
            }
        )

    # The batch ID is also the folder-like path segment.
    slug = normalize_batch_name(batch_name)
    batch_id = f"{slug}-{uuid4().hex[:8]}"
    prefix = get_batch_prefix(batch_id)

    uploaded_files = []

    for item in prepared_files:
        blob_name = f"{prefix}/{item['filename']}"

        await run_in_threadpool(
            upload_bytes,
            blob_name,
            item["content"],
            item["content_type"],
        )

        uploaded_files.append(
            {
                "filename": item["filename"],
                "blob_name": blob_name,
                "size_bytes": len(item["content"]),
            }
        )

    manifest = {
        "batch_id": batch_id,
        "batch_name": batch_name.strip(),
        "status": "uploaded",
        "file_count": len(uploaded_files),
        "files": uploaded_files,
    }

    await run_in_threadpool(
        save_json,
        f"{prefix}/_batch.json",
        manifest,
    )

    return {
        "message": "Contract batch uploaded successfully.",
        **manifest,
        "process_endpoint": f"/contracts/batches/{batch_id}/process",
    }


@router.post("/batches/{batch_id}/process")
async def process_contract_batch(batch_id: str):
    """
    Extract text and tables from every uploaded document in a batch.

    Extracted Markdown is saved alongside the batch under 'processed/'.
    """

    # Validate the batch ID before using it in a storage path.
    if not re.fullmatch(r"[a-z0-9_-]+", batch_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid batch ID.",
        )

    prefix = get_batch_prefix(batch_id)
    manifest_name = f"{prefix}/_batch.json"

    exists = await run_in_threadpool(blob_exists, manifest_name)

    if not exists:
        raise HTTPException(
            status_code=404,
            detail="Contract batch not found.",
        )

    manifest = await run_in_threadpool(read_json, manifest_name)

    blob_names = await run_in_threadpool(list_blob_names, f"{prefix}/")

    # Only process original files, not the manifest or previous outputs.
    original_names = [
        name
        for name in blob_names
        if name != manifest_name
        and "/processed/" not in name
        and Path(name).suffix.lower()
        in settings.allowed_extension_set
    ]

    if not original_names:
        raise HTTPException(
            status_code=404,
            detail="No contract documents found in this batch.",
        )

    results = []
    failures = []

    for blob_name in original_names:
        filename = blob_name.rsplit("/", 1)[-1]

        try:
            file_bytes = await run_in_threadpool(
                download_bytes,
                blob_name,
            )

            extracted = await run_in_threadpool(
                extract_document,
                file_bytes,
                filename,
            )

            output_name = f"{prefix}/processed/{filename}.md"

            await run_in_threadpool(
                upload_bytes,
                output_name,
                extracted["markdown"].encode("utf-8"),
                "text/markdown",
            )

            results.append(
                {
                    "filename": filename,
                    "status": "processed",
                    "table_count": extracted["table_count"],
                    "extracted_characters": len(
                        extracted["markdown"]
                    ),
                    "output_blob": output_name,
                }
            )

        except Exception:
            # Log the exception in production; don't expose internal
            # storage paths or exception details to API callers.
            failures.append(
                {
                    "filename": filename,
                    "status": "failed",
                    "message": "Document extraction failed.",
                }
            )

    manifest["status"] = (
        "completed_with_errors" if failures else "processed"
    )
    manifest["processing_results"] = results
    manifest["processing_failures"] = failures

    await run_in_threadpool(
        save_json,
        manifest_name,
        manifest,
    )

    return {
        "batch_id": batch_id,
        "batch_name": manifest["batch_name"],
        "status": manifest["status"],
        "total_documents": len(original_names),
        "processed_count": len(results),
        "failed_count": len(failures),
        "results": results,
        "failures": failures,
        "message": (
            "Document extraction completed. "
            "The output contains extracted text and tables, "
            "ready for contract analysis."
        ),
    }
