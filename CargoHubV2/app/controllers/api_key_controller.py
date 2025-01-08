from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.api_key_service import APIKeyService

# Create the router with prefix and tags
router = APIRouter(
    prefix="/api/v2/api-keys",
    tags=["API Keys"]
)


@router.post("/")
def create_api_key(
    key: str,
    access_scope: str,
    expires_in_days: int,  # Additional condition to accept an API key in the header
    db: Session = Depends(get_db),
    api_key: str = Header(...),
):
    # Initialize the APIKeyService and create the API key
    service = APIKeyService(db)
    created_key = service.create_api_key(key, access_scope, expires_in_days)

    return {"id": created_key.id, "expires_at": created_key.expires_at}


@router.get("/{key_id}")
def get_api_key(
    key_id: str,
    # Additional condition to accept an API key in the header
    api_key: str = Header(...),
    db: Session = Depends(get_db)
):

    # Initialize the APIKeyService and retrieve the API key
    service = APIKeyService(db)
    api_key_data = service.get_api_key(key_id)
    if not api_key_data:
        raise HTTPException(status_code=404, detail="API key not found")

    return {
        "id": api_key_data.id,
        "access_scope": api_key_data.access_scope,
        "created_at": api_key_data.created_at,
        "expires_at": api_key_data.expires_at,
        "last_used_at": api_key_data.last_used_at,
    }


@router.delete("/{key_id}")
def delete_api_key(
    key_id: str,
    # Additional condition to accept an API key in the header
    api_key: str = Header(...),
    db: Session = Depends(get_db)
):

    # Initialize the APIKeyService and delete the API key
    service = APIKeyService(db)
    success = service.delete_api_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")

    return {"detail": "API key deleted successfully"}
