from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def check_day_validity(date: str):
    try:
        valid_date = datetime.strptime(date, "%Y-%m-%d")
        return valid_date
    except ValueError:
        # bij invalide format gelijk bad request
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="dates for filter mus be in format YYYY-MM-DD")


def report_current_month(db: Session, offset: int, limit: int):
    pass


def report_between_dates(db: Session, dates: list[str], offset: int, limit: int):
    date_from, date_to = check_day_validity(dates[0], dates[1])
    pass


def report_for_warehouse(db: Session, warehouse_code: str, dates: list[str], offset: int, limit: int):
    # dates kan hier None zijn, eerst checken
    if (dates):
        date_from, date_to = check_day_validity(dates[0], dates[1])
    pass
