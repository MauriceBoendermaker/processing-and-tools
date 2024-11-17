from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.api_keys_model import APIKey

def validate_api_key(required_permission: str, x_api_key: str = Header(...), db: Session = Depends(get_db)):
    """
    Middleware to validate API key and permissions.
    - required_permission: Permission required to perform the action.
    """
    api_key = db.query(APIKey).filter(APIKey.key == x_api_key, APIKey.is_active == True).first()
    if not api_key:
        raise HTTPException(status_code=403, detail="Invalid or inactive API key")

    if required_permission not in api_key.permissions:
        raise HTTPException(status_code=403, detail="Permission denied for this action")

    return api_key  # Return the API key object for further use if needed
