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

if "hazard_classification" not in items_table.columns:
    raise Exception("Column 'hazard_classification' does not exist in 'items' table.")

with engine.begin() as conn:
    results = conn.execute(select(items_table)).mappings().all()
    
    # Randomize de boel
    for row in results:
        item_id = row["uid"]
        random_hazard = random.choice(hazard_classes)
        
        conn.execute(
            items_table.update()
            .where(items_table.c.uid == item_id)
            .values(hazard_classification=random_hazard)
        )
        print(f"Updated item UID {item_id} with hazard classification '{random_hazard}'")

print("Hazard classifications populated!")
