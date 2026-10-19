from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Vendor Contract Analysis API"
    log_level: str = "INFO"

    azure_storage_connection_string: str
    azure_storage_container_name: str

    max_upload_size_mb: int = 25
    max_files_per_batch: int = 20
    allowed_extensions: str = ".pdf,.docx,.md,.txt"
    contract_documents_prefix: str = "contract_documents"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_extension_set(self) -> set[str]:
        return {
            ext.strip().lower()
            for ext in self.allowed_extensions.split(",")
            if ext.strip()
        }


settings = Settings()