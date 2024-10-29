from fastapi import FastAPI
from app.controllers import warehouse_controller

app = FastAPI()
# welke port hij runt kan je bij command aanpassen
# default port is localhost:8000

# router van de controller gebruiken
app.include_router(warehouse_controller.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def stat():
    return {"status": "originele data hebben en controllers maken"}
