import os
from dotenv import load_dotenv

load_dotenv()  # laad configs in uit .env bestand

DATABASE_URL = os.getenv("DATABASE_URL")
