

from api.routes.contracts import router as contracts_router
from src.app.config import settings

import subprocess

result = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)

print(result.stdout)
print(result.stderr)


from fastapi import FastAPI
app = FastAPI(
    title=settings.app_name,
    description=(
        "Upload vendor contract batches, extract document text "
        "and tables, and prepare documents for AI analysis."
    ),
    version="1.0.0",
)

app.include_router(contracts_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
