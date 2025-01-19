# api_dependencies.py

from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

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
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid or unauthorized API key")

def role_required(allowed_roles: List[str]):
    """
    Returns a dependency that:
    1. Depends on get_valid_api_key (ensuring the key is valid).
    2. Checks current_api_key.access_scope is in allowed_roles.
    3. Raises 403 if not.
    """
    def wrapper(current_api_key: APIKey = Depends(get_valid_api_key)) -> APIKey:
        if current_api_key.access_scope not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=(
                    f"Insufficient role. Allowed: {allowed_roles}, "
                    f"got: {current_api_key.access_scope}"
                ),
            )
        return current_api_key
    return wrapper
