"""FastAPI application.

Every route added here must first exist in contracts/openapi.yaml.
tests/contract/test_openapi.py fails the build otherwise (CI gate 1).
"""

from fastapi import FastAPI

app = FastAPI(title="Optata Core API", docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
