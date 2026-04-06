from fastapi import FastAPI


app = FastAPI(title="Eggscaliber API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
