from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.api_keys_model import APIKey

def seed_api_keys(db: Session):
    # Predefined API keys and roles
    keys = [
        {
            "key": "manager_api_key_12345",
            "role": "manager",
            "permissions": ["create", "delete", "edit"]
        },
        {
            "key": "floor_manager_api_key_67890",
            "role": "floor_manager",
            "permissions": ["create", "edit"]
        },
        {
            "key": "medewerker_api_key_11223",
            "role": "medewerker",
            "permissions": ["view"]
        },
    ]

    # Add keys to the database if they don't exist
    for key_data in keys:
        existing_key = db.query(APIKey).filter(APIKey.key == key_data["key"]).first()
        if not existing_key:
            print(f"Adding key: {key_data['key']} with role {key_data['role']}")
            api_key = APIKey(
                key=key_data["key"],
                role=key_data["role"],
                permissions=key_data["permissions"],
                is_active=True
            )
            db.add(api_key)
    db.commit()
    print("Seeding completed.")

# Main script entry point
if __name__ == "__main__":
    print("Connecting to the database...")
    db = SessionLocal()  # Create a new database session
    try:
        seed_api_keys(db)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()  # Ensure the session is closed
    print("Database session closed.")
