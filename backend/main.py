from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="eTech RFP Workbench API", version="0.1.0")


class AnalyzeRequest(BaseModel):
    solicitation_text: str
    customer_name: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/config")
def config() -> dict[str, str]:
    return {"app": "eTech RFP Workbench", "mode": "baseline"}


@app.post("/api/rfp/analyze")
def analyze_rfp(request: AnalyzeRequest) -> dict[str, str]:
    _ = request
    return {
        "status": "not_implemented",
        "message": "Analysis pipeline has not yet been restored from the target deployment.",
    }
