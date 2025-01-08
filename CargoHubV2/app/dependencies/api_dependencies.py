# api_dependencies.py

from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from CargoHubV2.app.services.api_key_service import APIKeyService
from CargoHubV2.app.models.api_key_model import APIKey


def get_valid_api_key(
    api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> APIKey:

    service = APIKeyService(db)

    try:
        return service.validate_api_key(api_key)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid or unauthorized API key")
