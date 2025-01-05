import random
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///Cargo_Database.db"

# Gevaar classes
hazard_classes = [
    "Flammable",
    "Explosive",
    "Toxic",
    "Non-hazardous",
    "Corrosive",
    "Radioactive",
    "Oxidizing",
    "Infectious",
    "Combustible",
    "Compressed gas"
]

# Set up voor SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

metadata.reflect(bind=engine)

items_table = metadata.tables["items"]
