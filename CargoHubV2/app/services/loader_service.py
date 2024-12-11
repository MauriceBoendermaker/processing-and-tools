from CargoHubV2.app.models import *
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from CargoHubV2.app.models import (items_model, item_groups_model, item_lines_model,
#                                    item_types_model, warehouses_model, transfers_model,
#                                    locations_model, suppliers_model, shipments_model, 
#                                    clients_model, inventories_model, orders_model)
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
        "inventories.json": inventories_model.Inventory,
        "orders.json": orders_model.Order
    }


def load(path: str, db: Session):
    base_dir = os.path.abspath(os.path.join(__file__, "C:/Users/mauri/source/repos/HR Jaar 2/CargoHub"))

    for file in model_mapping:
        json_file_path = os.path.join(base_dir, "data", file)

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        id_tracker = set()

        for num, record in tqdm(enumerate(data, start=1), desc=f"Processing {file}"):
            if file == "orders.json":
                original_id = record["id"]

                while record["id"] in id_tracker:
                    record["id"] = num
                
                id_tracker.add(record["id"])
                if record["id"] != original_id:
                    print(f"Adjusted ID from {original_id} to {record['id']}")

            try:
                # Parse datetime fields
                if "created_at" in record:
                    record["created_at"] = parse_iso_datetime(record["created_at"])
                if "updated_at" in record:
                    record["updated_at"] = parse_iso_datetime(record["updated_at"], default_now=True)
                if "order_date" in record:
                    record["order_date"] = parse_iso_datetime(record["order_date"])
                if "request_date" in record:
                    record["request_date"] = parse_iso_datetime(record["request_date"])
                if "shipment_date" in record:
                    record["shipment_date"] = parse_iso_datetime(record["shipment_date"])

                # Handle nested JSON fields (e.g., items)
                if "items" in record and isinstance(record["items"], (list, dict)):
                    record["items"] = json.dumps(record["items"])

                obj = model_mapping[file](**record)
                db.add(obj)

            except Exception as e:
                db.rollback()
                print(f"Error inserting record: {record}\n{e}")

    try:
        db.commit()
        return "Data successfully loaded."
    except SQLAlchemyError as e:
        db.rollback()
        print(f"error detected: {e}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    return "hij is klaar met loaden"


def parse_iso_datetime(value, default_now=False):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                if default_now:
                    return datetime.now()
                raise ValueError(f"Invalid datetime format: {value}")