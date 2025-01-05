from sqlalchemy import create_engine, MetaData, select

DATABASE_URL = "sqlite:///CargoHubV2/Cargo_Database.db"

# Set up voor SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()

metadata.reflect(bind=engine)

inventories_table = metadata.tables["inventories"]
locations_table = metadata.tables["locations"]

with engine.begin() as conn:
    # Iventories
    inven_results = conn.execute(select(inventories_table)).mappings().all()

    # door elke inventory voor voorraad
    for row in inven_results:
        loc_ids = row["locations"]
        if len(loc_ids) == 0:
            continue
        voorraad = {row["item_id"]: row["total_on_hand"]}

        conn.execute(
            locations_table.update()
            .where(locations_table.c.id == loc_ids[0])
            .values(stock=voorraad)
        )
        print(f"Updated location {loc_ids[0]} with stock {voorraad}")

    loc_results = conn.execute(select(locations_table)).mappings().all()
    for row in loc_results:
        if row["stock"] is None:
            conn.execute(
            locations_table.update()
            .where(locations_table.c.id == row["id"])
            .values(stock={"empty": 0})
        )


# \/\/ stelde de docent voor
print("elke inventories voorraad is in de eeerste locatie gegooid")
