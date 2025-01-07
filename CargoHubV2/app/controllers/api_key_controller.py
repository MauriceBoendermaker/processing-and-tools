from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from CargoHubV2.app.database import get_db
from CargoHubV2.app.services.api_key_service import APIKeyService
from utils.encryption_util import EncryptionUtility

router = APIRouter()

def get_encryption_utility():
    from dotenv import load_dotenv
    import os
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY not set in environment variables")
    return EncryptionUtility(secret_key=SECRET_KEY)

@router.post("/api-keys/")
def create_api_key(
    key: str,
    access_scope: str,
    expires_in_days: int,
    db: Session = Depends(get_db),
    encryption_utility: EncryptionUtility = Depends(get_encryption_utility),
):
    service = APIKeyService(db, encryption_utility)
    api_key = service.create_api_key(key, access_scope, expires_in_days)
    return {"id": api_key.id, "expires_at": api_key.expires_at}

@router.get("/api-keys/{key_id}")
def get_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    encryption_utility: EncryptionUtility = Depends(get_encryption_utility),
):
    service = APIKeyService(db, encryption_utility)
    api_key = service.get_api_key(key_id)
    if api_key:
        return {
            "id": api_key.id,
            "access_scope": api_key.access_scope,
            "created_at": api_key.created_at,
            "expires_at": api_key.expires_at,
            "last_used_at": api_key.last_used_at,
        }
    return {"error": "API key not found"}
