from fastapi import FastAPI, Request, HTTPException, Response
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
from CargoHubV2.app.controllers import reporting_controller
from CargoHubV2.app.controllers import packinglist_controller
from CargoHubV2.app.controllers import docks_controller

import os
from dotenv import load_dotenv
from starlette.responses import JSONResponse
import logging


app = FastAPI()
# welke port hij runt kan je bij command aanpassen
# default port is localhost:8000

# router van de controller gebruiken
app.include_router(reporting_controller.router)
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
app.include_router(packinglist_controller.router)
app.include_router(docks_controller.router)

logger = logging.getLogger("uvicorn.error")

# haalt api keys uit env variabelen
# in github werkt dit ook, uit GH secrets
# voor lokaal runnen, moet er een .env zijn met deze 3 variabelen
load_dotenv()
warehouse_manager = os.getenv("WAREHOUSE_MANAGER")
floor_manager = os.getenv("FLOOR_MANAGER")
employee = os.getenv("EMPLOYEE")
print(warehouse_manager)
print(floor_manager)
print(employee)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def stat():
    return {"status": "originele data hebben en controllers maken"}


@app.on_event("shutdown")
async def shutdown():
    # Close any resources (e.g., database connections, files, sockets) here
    print("Shutting down gracefully...")


@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    # anders kan de documentatie niet bereikt worden
    excluded = ["/favicon.ico", "/openapi.json", "/docs"]

    try:
        x_api_key = request.headers.get("api-key")
        if request.url.path in excluded:
            return await call_next(request)
        response: Response = await call_next(request)

        if not x_api_key:
            logger.warning("Missing API key")
            response.status_code = 422
            raise HTTPException(status_code=422, detail="Missing API key")

        if x_api_key != "a1b2c3d4e5":
            logger.warning("Invalid API key")
            response.status_code = 403
            raise HTTPException(status_code=403, detail="Invalid API key")

        return response

    except HTTPException as http_exc:

        logger.error(f"HTTPException raised: {http_exc.detail}")
        return JSONResponse(
            status_code=http_exc.status_code, content={"detail": http_exc.detail}
        )
    except Exception as exc:
        logger.exception("Unexpected error occurred in middleware")
        raise exc
