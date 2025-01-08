from sqlalchemy.orm import Session
from uuid import uuid4
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from CargoHubV2.app.models.api_key_model import APIKey
from CargoHubV2.app.utils.encryption_util import EncryptionUtility


class APIKeyService:
    def __init__(self, db: Session):
        # Load the .env file and SECRET_KEY
        load_dotenv()
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise RuntimeError("SECRET_KEY not set in .env or environment variables")
        # Initialize encryption utility with the loaded SECRET_KEY
        self.encryption_utility = EncryptionUtility(secret_key=secret_key)
        self.db = db

    def create_api_key(self, key: str, access_scope: str, expires_in_days: int):
        """Create and store a new encrypted API key."""
        encrypted_key = self.encryption_utility.encrypt(key)
        api_key = APIKey(
            id=str(uuid4()),  # Generate a unique ID for the API key
            encrypted_key=encrypted_key,  # Store the encrypted key
            access_scope=access_scope,  # Permissions associated with the key
            created_at=datetime.utcnow(),  # Set creation timestamp
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),  # Set expiration
        )
        self.db.add(api_key)
        self.db.commit()
        return api_key
    
    def validate_api_key(self, raw_api_key: str) -> APIKey:
        """
        1. Decrypt or just compare if you store plaintext vs. encrypted.
        2. Check if the key is in the DB.
        3. Check expiration, update last_used_at, etc.
        4. If invalid, raise an exception (which we can catch in the dependency).
        """
        # If you're storing the encrypted version in DB, you might do something like:
        encrypted_input = self.encryption_utility.encrypt(raw_api_key)

        api_key_data = (
            self.db.query(APIKey)
            .filter(APIKey.encrypted_key == encrypted_input)
            .first()
        )
        if not api_key_data:
            raise ValueError("API key not found")

        # Check expiration
        if api_key_data.expires_at and api_key_data.expires_at < datetime.utcnow():
            raise ValueError("API key has expired")

        # Update last used
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
