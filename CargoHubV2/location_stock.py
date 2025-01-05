import random
import json
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///../Cargo_Database.db"

# maximum gewichten
hazard_classes = {"laag": 10}

# Set up voor SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

metadata.reflect(bind=engine)

items_table = metadata.tables["items"]
warehouses_table = metadata.tables["warehouses"]

if "hazard_classification" not in items_table.columns:
    raise Exception("Column 'hazard_classification' does not exist in 'items' table.")

if "forbidden_classifications" not in warehouses_table.columns:
    raise Exception("Column 'forbidden_classifications' does not exist in 'warehouses' table.")

with engine.begin() as conn:
    # Items
    item_results = conn.execute(select(items_table)).mappings().all()

    # Randomize de boel
    for row in item_results:
        item_id = row["uid"]
        random_hazard = random.choice(hazard_classes)
        
        conn.execute(
            items_table.update()
            .where(items_table.c.uid == item_id)
            .values(hazard_classification=random_hazard)
        )
        print(f"Updated item UID {item_id} with hazard classification '{random_hazard}'")

    # Warehouse
    warehouse_results = conn.execute(select(warehouses_table)).mappings().all()

    # Randomize de boel
    for warehouse in warehouse_results:
        warehouse_id = warehouse["id"]
        
        forbidden_object = {
            hazard: random.choice([True, False]) for hazard in hazard_classes
        }
        
        conn.execute(
            warehouses_table.update()
            .where(warehouses_table.c.id == warehouse_id)
            .values(forbidden_classifications=json.dumps(forbidden_object))
        )
        print(f"Updated warehouse ID {warehouse_id} with forbidden classifications {forbidden_object}")

print("Populated hazard classifications and forbidden classifications!")