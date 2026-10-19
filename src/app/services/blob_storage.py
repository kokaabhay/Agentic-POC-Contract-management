
import json
from typing import Any

from azure.storage.blob import BlobServiceClient, ContentSettings

from src.app.config import settings


blob_service_client = BlobServiceClient.from_connection_string(
    settings.azure_storage_connection_string
)

container_client = blob_service_client.get_container_client(
    settings.azure_storage_container_name
)


def upload_bytes(
    blob_name: str,
    content: bytes,
    content_type: str = "application/octet-stream",
) -> None:
    blob_client = container_client.get_blob_client(blob_name)

    blob_client.upload_blob(
        content,
        overwrite=False,
        content_settings=ContentSettings(
            content_type=content_type
        ),
    )


def download_bytes(blob_name: str) -> bytes:
    blob_client = container_client.get_blob_client(blob_name)
    return blob_client.download_blob().readall()


def list_blob_names(prefix: str) -> list[str]:
    return [
        blob.name
        for blob in container_client.list_blobs(
            name_starts_with=prefix
        )
    ]


def blob_exists(blob_name: str) -> bool:
    return container_client.get_blob_client(blob_name).exists()


def save_json(blob_name: str, data: dict[str, Any]) -> None:
    content = json.dumps(data, indent=2).encode("utf-8")

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(
        content,
        overwrite=True,
        content_settings=ContentSettings(
            content_type="application/json"
        ),
    )


def read_json(blob_name: str) -> dict[str, Any]:
    content = download_bytes(blob_name)
    return json.loads(content.decode("utf-8"))
