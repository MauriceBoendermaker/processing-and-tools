from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from CargoHubV2.app.dependencies.api_dependencies import get_valid_api_key
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.api_key_service import APIKeyService
from CargoHubV2.app.models.api_key_model import APIKey


# Create the router with prefix and tags
router = APIRouter(
    prefix="/api/v2/api-keys",
    tags=["API Keys"]
)


@router.post("/")
def create_api_key(
    key: str,
    access_scope: str,
    expires_in_days: int,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(get_valid_api_key),
):
    """Create a new API key."""
    # Optional: If you want only 'admin' scope to create keys, check:
    # if 'admin' not in current_api_key.access_scope.split(','):
    #     raise HTTPException(status_code=403, detail="Insufficient scope.")

    service = APIKeyService(db)
    created_key = service.create_api_key(key, access_scope, expires_in_days)
    return {"id": created_key.id, "expires_at": created_key.expires_at}


@router.get("/{key_id}")
def get_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(get_valid_api_key),
):
    service = APIKeyService(db)
    api_key_data = service.get_api_key(key_id)
    if not api_key_data:
        raise HTTPException(status_code=404, detail="API key not found")
    return api_key_data


@router.delete("/{key_id}")
def delete_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    current_api_key: APIKey = Depends(get_valid_api_key),
):
    service = APIKeyService(db)
    success = service.delete_api_key(key_id)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"detail": "API key deleted successfully"}