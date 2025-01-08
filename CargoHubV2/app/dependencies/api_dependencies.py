# api_dependencies.py

from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

# Adjust imports to match your project
from ..database import get_db
from CargoHubV2.app.services.api_key_service import APIKeyService
from CargoHubV2.app.models.api_key_model import APIKey


def get_valid_api_key(
    api_key: str = Header(...),
    db: Session = Depends(get_db)
) -> APIKey:
    """
    Reads the `api_key` from the request header, calls our
    service to validate it, and returns the APIKey object
    if valid. Raises HTTPException otherwise.
    """

    service = APIKeyService(db)

    # Let's assume your service has a method like `validate_api_key()`
    # that raises an exception if the key is invalid/expired.
    try:
        return service.validate_api_key(api_key)
    except ValueError as e:
        # If you decide to raise custom exceptions in your service,
        # you can catch them here and convert them to HTTPException.
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        # Fallback catch-all
        raise HTTPException(status_code=403, detail="Invalid or unauthorized API key")
