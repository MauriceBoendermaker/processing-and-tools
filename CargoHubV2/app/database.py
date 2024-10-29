# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# environment variabelen inladen
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# nieuw sqlite engine, hoort bij sqlalchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# voor database sessions in fastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
