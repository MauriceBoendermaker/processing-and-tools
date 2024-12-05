from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services import reporting_service
from typing import List, Optional

router = APIRouter(
    prefix="/api/v2/reports",
    tags=["reports"]
)


@router.get("/{warehouse_code}")
def generate_report_by_warehouse(
    warehouse_code: str,
    db: Session = Depends(get_db),
    offset: int = 0,
    dates: list[str] = None,
        limit: int = 100):

    return reporting_service.report_for_warehouse(db, warehouse_code, offset, limit)


@router.get("/")
def generate_general_report(
    db: Session = Depends(get_db),
    dates: list[str] = None,
    offset: int = 0,
        limit: int = 100):
    if not dates:
        return reporting_service.report_current_month(db, offset, limit)
    return reporting_service.report_between_dates(db, dates, offset, limit)
