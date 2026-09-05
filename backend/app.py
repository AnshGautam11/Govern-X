"""
GovernX backend entrypoint.

Run locally:
    uvicorn app:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config.settings import get_settings
from models.schemas import ScanResponse

settings = get_settings()

app = FastAPI(
    title="GovernX API",
    description="Automated NIST CSF 2.0 compliance and risk quantification engine",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type"],
)


@app.get("/health")
def health_check():
    """Basic liveness check."""
    return {"status": "ok", "service": "GovernX", "env": settings.environment}


@app.post("/scan/aws", response_model=ScanResponse)
def run_aws_scan():
    """
    Trigger the AWS collector, run all registered checks, map results to
    NIST CSF 2.0 subcategories, and return the findings.

    Week 2: results are also persisted to the scan_results table
    (see database/persistence.py) so /scan/history can list past scans.
    """
    from collectors.aws_collector import run_all_checks
    from database.persistence import save_scan_results

    try:
        results = run_all_checks()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="AWS scan is currently unavailable. Check backend AWS permissions and configuration.",
        ) from exc

    save_scan_results(results)

    return ScanResponse(results=results)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
