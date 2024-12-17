from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.loader_service import load
from typing import Optional, List

router = APIRouter(
    prefix="/api/v2/load",
    tags=["loader"]
)


@router.post("/",)
def load_from_json(path, db: Session = Depends(get_db), api_key: str = Header(...)):
    return load(path, db)
