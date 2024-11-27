from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.api_keys_model import APIKey

import os
from dotenv import load_dotenv
from pathlib import Path


def validate_api_key(required_permission: str, x_api_key: str = Depends(), db: Session = Depends(get_db)):
    base_dir = Path(__file__).resolve().parents[2]  # Adjust this if the nesting changes
    dotenv_path = base_dir / ".env"

    # Load the .env file
    load_dotenv(dotenv_path)

    # Retrieve the ADMIN variable
    admin = os.getenv("ADMIN")

    if not x_api_key or x_api_key != admin:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")



    api_key = db.query(APIKey).filter(APIKey.key == x_api_key, APIKey.is_active == True).first()

    '''
    if not api_key:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

    if required_permission not in api_key.permissions:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    '''
