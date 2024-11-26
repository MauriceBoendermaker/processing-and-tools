from fastapi import FastAPI
from CargoHubV2.app.controllers import item_groups
from CargoHubV2.app.controllers import item_lines
from CargoHubV2.app.controllers import item_types
from CargoHubV2.app.controllers import items_controller
from CargoHubV2.app.controllers import locations_controller
from CargoHubV2.app.controllers import transfers_controller
from CargoHubV2.app.controllers import suppliers_controller
from CargoHubV2.app.controllers import warehouses_controller
from CargoHubV2.app.controllers import load_controller
from CargoHubV2.app.controllers import clients_controller
from CargoHubV2.app.controllers import shipments_controller
from CargoHubV2.app.controllers import inventories_controller
from CargoHubV2.app.controllers import orders_controller


app = FastAPI()
# welke port hij runt kan je bij command aanpassen
# default port is localhost:8000

# router van de controller gebruiken
app.include_router(item_groups.router)
app.include_router(item_lines.router)
app.include_router(item_types.router)
app.include_router(items_controller.router)
app.include_router(locations_controller.router)
app.include_router(transfers_controller.router)
app.include_router(suppliers_controller.router)
app.include_router(warehouses_controller.router)
app.include_router(load_controller.router)
app.include_router(clients_controller.router)
app.include_router(shipments_controller.router)
app.include_router(inventories_controller.router)
app.include_router(orders_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def stat():
    return {"status": "originele data hebben en controllers maken"}

'''

# script voor migrations voor later
from database import Base, engine
from models import warehouse_model, items_model, location_model, transfers_model # alle models die je wil migraten


# maakt alle tables
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Tables created successfully!")
'''
