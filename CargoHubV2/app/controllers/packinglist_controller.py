from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services import packinglist_service
from CargoHubV2.app.models.orders_model import Order
from fastapi.responses import FileResponse
from pathlib import Path

from CargoHubV2.app.dependencies.api_dependencies import (
    get_valid_api_key,
    role_required
)
from CargoHubV2.app.models.api_key_model import APIKey

router = APIRouter(
    prefix="/api/v2/packinglist",
    tags=["packinglist"]
)

@router.get("/api/v2/packinglist/{order_id}")
def create_packing_list(
    order_id: int, 
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return packinglist_service.generate_packing_list(order)


@router.get("/get-pdf/{filename}")
def get_pdf(filename: str):
    PDF_DIR = Path("generated_pdfs")
    pdf_path = PDF_DIR/filename
    if pdf_path.exists():
        return FileResponse(pdf_path, media_type="application/pdf", filename=filename)
    else:
        raise HTTPException(status_code=404, detail="PDF not found")