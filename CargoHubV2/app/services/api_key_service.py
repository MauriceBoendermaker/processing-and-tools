from sqlalchemy.orm import Session
from uuid import uuid4
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from CargoHubV2.app.models.api_key_model import APIKey
from CargoHubV2.app.utils.hashing_util import HashingUtility


class APIKeyService:
    def __init__(self, db: Session):
        load_dotenv()
        secret_key = os.getenv("SECRET_KEY")  # optional
        if not secret_key:
            # If you want a fallback, you could do: secret_key = "some_default"
            raise RuntimeError("SECRET_KEY not set in .env or environment variables")

        self.hashing_utility = HashingUtility(secret_key=secret_key)
        self.db = db

    def create_api_key(self, key: str, access_scope: str, expires_in_days: int):
        """Create and store a new hashed API key."""
        hashed_key = self.hashing_utility.hash_data(key)
        api_key = APIKey(
            id=str(uuid4()),  # Generate unique ID
            encrypted_key=hashed_key,  # If you haven't renamed the column, just reuse 'encrypted_key'
            access_scope=access_scope,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
        )
        self.db.add(api_key)
        self.db.commit()
        return api_key

    def validate_api_key(self, raw_api_key: str) -> APIKey:
        """
        1. Hash the incoming API key
        2. Look up the DB record by the hashed value
        3. Check expiration, update last_used_at
        4. Return the APIKey record or raise an exception
        """
        hashed_input = self.hashing_utility.hash_data(raw_api_key)

        api_key_data = (
            self.db.query(APIKey)
            .filter(APIKey.encrypted_key == hashed_input)
            .first()
        )
        if not api_key_data:
            raise ValueError("API key not found")

        if api_key_data.expires_at and api_key_data.expires_at < datetime.utcnow():
            raise ValueError("API key has expired")

        # Optional: update last_used_at
        api_key_data.last_used_at = datetime.utcnow()
        self.db.commit()

        return api_key_data

    def get_api_key(self, key_id: str):
        """Retrieve an API key by its ID."""
        return self.db.query(APIKey).filter(APIKey.id == key_id).first()

    def update_last_used(self, key_id: str):
        """Update the last used timestamp for an API key."""
        api_key = self.get_api_key(key_id)
        if api_key:
            api_key.last_used_at = datetime.utcnow()
            self.db.commit()
        return api_key

    def delete_api_key(self, key_id: str):
        """Delete an API key by its ID."""
        api_key = self.get_api_key(key_id)
        if api_key:
            self.db.delete(api_key)
            self.db.commit()
            return True
        return False
