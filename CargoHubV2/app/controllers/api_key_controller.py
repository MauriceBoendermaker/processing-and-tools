from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.api_key_service import APIKeyService
from utils.encryption_util import EncryptionUtility
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set in environment variables")

# Initialize FastAPI app and dependencies
app = FastAPI()
encryption_utility = EncryptionUtility(secret_key=SECRET_KEY)

@app.post("/api-keys/")
def create_api_key(
    key: str,
    access_scope: str,
    expires_in_days: int,
    db: Session = Depends(get_db)
):
    service = APIKeyService(db, encryption_utility)
    api_key = service.create_api_key(key, access_scope, expires_in_days)
    return {"id": api_key.id, "expires_at": api_key.expires_at}

@app.get("/api-keys/{key_id}")
def get_api_key(
    key_id: str,
    db: Session = Depends(get_db)
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
