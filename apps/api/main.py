"""Eggscaliber API entrypoint.

Dataset metadata lifecycle contracts live in `apps.api.metadata_domain` (STU-117).
HTTP routes for that flow ship in later build slices.
"""

from fastapi import FastAPI

app = FastAPI(title="Eggscaliber API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
