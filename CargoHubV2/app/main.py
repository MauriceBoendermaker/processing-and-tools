'''
from fastapi import FastAPI
from CargoHubV2.app.controllers import warehouse_controller
from CargoHubV2.app.controllers import location_controller
from CargoHubV2.app.controllers import items_controller
from CargoHubV2.app.controllers import transfer_controller

app = FastAPI()
# welke port hij runt kan je bij command aanpassen
# default port is localhost:8000

# router van de controller gebruiken
app.include_router(warehouse_controller.router)
app.include_router(location_controller.router)
app.include_router(items_controller.router)
app.include_router(transfer_controller.router)


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
