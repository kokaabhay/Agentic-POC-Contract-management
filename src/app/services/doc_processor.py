import tempfile
from pathlib import Path

from docling.document_converter import DocumentConverter

converter = DocumentConverter()

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".md", ".txt"}


def extract_document(file_bytes: bytes, filename: str) -> dict:
    """
    Extract text and tables from a supported document.

    Args:
        file_bytes: The original document content as bytes.
        filename: The original document filename.

    Returns:
        A dictionary containing the filename, extracted Markdown,
        and table count.
    """
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {extension}")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=extension,
            delete=False,
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        result = converter.convert(temp_path)
        document = result.document

        markdown = document.export_to_markdown()

        return {
            "filename": filename,
            "markdown": markdown,
            "table_count": len(document.tables),
        }

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)