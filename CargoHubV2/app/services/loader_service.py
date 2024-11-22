from CargoHubV2.app.models import *
from fastapi import HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from CargoHubV2.app.models import (items_model, item_groups_model, item_lines_model,
                                   item_types_model, warehouses_model, transfers_model,
                                   locations_model, suppliers_model, shipments_model, 
                                   clients_model, inventories_model)
import os
import json
from tqdm import tqdm

model_mapping = {
        "items.json": items_model.Item,
        "item_groups.json": item_groups_model.ItemGroup,
        "item_lines.json": item_lines_model.ItemLine,
        "item_types.json": item_types_model.ItemType,
        "warehouses.json": warehouses_model.Warehouse,
        "transfers.json": transfers_model.Transfer,
        "locations.json": locations_model.Location,
        "suppliers.json": suppliers_model.Supplier,
        "shipments.json": shipments_model.Shipment,
        "clients.json": clients_model.Client,
        "inventories.json": inventories_model.Inventory
    }


def load(path: str, db: Session):
    base_dir = os.path.abspath(os.path.join(__file__, "../../../../.."))

    for file in model_mapping:

        # path naar json
        json_file_path = os.path.join(base_dir, "data", file)

        # file openen en loaden
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        for i in tqdm(data):
            if (file == "transfers.json" or file == "shipments.json" or file == "orders.json"):
                i["created_at"] = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                i["updated_at"] = datetime.strptime(i["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
            else:
                i["created_at"] = datetime.strptime(i["created_at"], "%Y-%m-%d %H:%M:%S")
                i["updated_at"] = datetime.now()
            obj = model_mapping[file](**i)
            db.add(obj)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(f"error detected: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    return "hij is klaar met loaden"
