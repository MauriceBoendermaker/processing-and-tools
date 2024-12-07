from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services import reporting_service
from typing import List, Optional

router = APIRouter(
    prefix="/api/v2/reports",
    tags=["reports"]
)


@router.get("/{warehouse_id}")
def generate_report_by_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    year_to_report: int = 2024,
        month_to_report: int = 9):

    return reporting_service.report_for_warehouse(db, warehouse_id, year_to_report, month_to_report)


@router.get("/")
def generate_general_report(
    db: Session = Depends(get_db),
    year_to_report: int = 2024,
    month_to_report: int = 9,
    offset: int = 0,
        limit: int = 100):
    return generate_general_report(db, year_to_report, month_to_report, offset, limit)
