from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.api_keys_model import APIKey

def validate_api_key(required_permission: str, x_api_key: str = Depends(), db: Session = Depends(get_db)):
    api_key = db.query(APIKey).filter(APIKey.key == x_api_key, APIKey.is_active == True).first()
    if not api_key:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    
    if required_permission not in api_key.permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
