from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services import reporting_service
from typing import List, Optional
from pathlib import Path

from CargoHubV2.app.dependencies.api_dependencies import (
    get_valid_api_key,
    role_required
)
from CargoHubV2.app.models.api_key_model import APIKey

router = APIRouter(
    prefix="/api/v2/reports",
    tags=["reports"]
)


@router.get("/{warehouse_id}")
def generate_report_by_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    year_to_report: int = 2024,
    api_key: str = Header(...),
        month_to_report: int = 9):

    response = reporting_service.report_for_warehouse(db, warehouse_id, year_to_report, month_to_report)
    return reporting_service.generate_pdf(response)


@router.get("/")
def generate_general_report(
    db: Session = Depends(get_db),
    year_to_report: int = 2024,
    month_to_report: int = 9,
    offset: int = 0,
    api_key: str = Header(...),
        limit: int = 100):

    response = reporting_service.general_report(db, year_to_report, month_to_report, offset, limit)
    return reporting_service.generate_pdf(response)


@router.get("/get-pdf/{filename}")
def get_pdf(filename: str):
    PDF_DIR = Path("generated_pdfs")
    pdf_path = PDF_DIR/filename
    if pdf_path.exists():
        return FileResponse(pdf_path, media_type="application/pdf", filename=filename)
    else:
        raise HTTPException(status_code=404, detail="PDF not found")
