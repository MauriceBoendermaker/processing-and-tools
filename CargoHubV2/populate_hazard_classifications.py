import random
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///Cargo_Database.db"
# Set up voor SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

metadata.reflect(bind=engine)

items_table = metadata.tables["items"]
