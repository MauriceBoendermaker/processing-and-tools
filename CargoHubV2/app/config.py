import os
from dotenv import load_dotenv

load_dotenv()  # laad configs in uit .env bestand

DATABASE_URL = os.getenv("DATABASE_URL")

# script voor migrations voor later
'''
from database import Base, engine
from models import warehouse_model  # Replace with your model modules

# maakt alle tables
Base.metadata.create_all(bind=engine)
'''
