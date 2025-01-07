from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from models.api_key_model import APIKey
from utils.encryption_util import EncryptionUtility

class APIKeyService:
    def __init__(self, db: Session, encryption_utility: EncryptionUtility):
        self.db = db
        self.encryption_utility = encryption_utility

    def create_api_key(self, key: str, access_scope: str, expires_in_days: int):
        encrypted_key = self.encryption_utility.encrypt(key)
        api_key = APIKey(
            id=str(uuid4()),
            encrypted_key=encrypted_key,
            access_scope=access_scope,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
        )
        self.db.add(api_key)
        self.db.commit()
        return api_key

    def get_api_key(self, key_id: str):
        return self.db.query(APIKey).filter(APIKey.id == key_id).first()

    def update_last_used(self, key_id: str):
        api_key = self.get_api_key(key_id)
        if api_key:
            api_key.last_used_at = datetime.utcnow()
            self.db.commit()
        return api_key
