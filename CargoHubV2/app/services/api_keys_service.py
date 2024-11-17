import secrets
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.api_keys_model import APIKey

def generate_api_key() -> str:
    """Generate a new random API key."""
    return secrets.token_hex(32)  # 64-character hex string

def create_api_key(user_id: int, db: Session, expires_at: datetime = None) -> str:
    """Create and store a new API key."""
    api_key = generate_api_key()
    new_key = APIKey(
        key=api_key,
        user_id=user_id,
        is_active=True,
        created_at=datetime.utcnow(),
        expires_at=expires_at
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    return api_key

def validate_api_key(key: str, db: Session) -> APIKey:
    """Validate an API key."""
    api_key = db.query(APIKey).filter(APIKey.key == key, APIKey.is_active == True).first()
    if not api_key:
        return None
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        return None
    return api_key

def revoke_api_key(key: str, db: Session) -> bool:
    """Revoke an API key by deactivating it."""
    api_key = db.query(APIKey).filter(APIKey.key == key).first()
    if not api_key:
        return False
    api_key.is_active = False
    db.commit()
    return True
