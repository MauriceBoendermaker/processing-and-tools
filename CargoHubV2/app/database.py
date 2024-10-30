# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# environment variabelen inladen
load_dotenv()

# database URL uit .env bestand halen
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
relative_db_url = os.getenv("DATABASE_URL")

# database path voor CargoHubV2 root
SQL_URL = relative_db_url.replace("sqlite:///./", f"sqlite:///{BASE_DIR}/")

# nieuw sqlite engine, hoort bij sqlalchemy
engine = create_engine(SQL_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# voor database sessions in fastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
