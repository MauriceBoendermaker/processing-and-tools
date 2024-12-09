import io
import os
import json
import pdfkit
import base64
import matplotlib.pyplot as plt

from pathlib import Path
from jinja2 import Template
from itertools import chain
from datetime import datetime
from sqlalchemy import extract
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, FastAPI
from CargoHubV2.app.models.orders_model import Order
from fastapi.responses import FileResponse, JSONResponse


PDF_DIR = Path("generated_pdfs")
PDF_DIR.mkdir(exist_ok=True)

TEMPLATE_FILE = Path(os.path.dirname(__file__)).parent / "report_template.html"

def generate_pdf(content: dict):
    try:
        pdf_content = json.dumps(content, indent=4)

        pdf_filename = f"report_for_{content.get("warehouse", "all")}_month_{content.get("target_month")}.pdf"
        pdf_path = PDF_DIR/pdf_filename

        pdfkit.from_string(pdf_content, str(pdf_path))

        # link naar de pdf
        pdf_url = f"http://127.0.0.1:3000/api/v2/reports/get-pdf/{pdf_filename}"

        return JSONResponse({"message": "report PDF generated successfully.", "pdf_url": pdf_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF, {e}")


def reporter(
        target_year: int,
        target_month: int,
        orders: list[Order],
        warehouse_id: int = -1):

    rauw = []
    for order in orders:
        if order.items:
            parsed_items = json.loads(order.items)
            rauw.append(parsed_items)
        else:
            rauw.append([])

    # chain maakt van een nested lijst een enkele lijst met alle inhoud
    items_totaal = sum(item["amount"] for item in list(chain.from_iterable(rauw)))

    if warehouse_id == -1:
        return {"target_month": f"{target_year}-{target_month}",
                "orders_done": f"{len(orders)}",
                "amount_of_items_sold": f"{items_totaal}",
                "total_revenue": f"{sum(order.total_amount for order in orders)}",
                "total_discount": f"{sum(order.total_discount for order in orders)}",
                "total_tax": f"{sum(order.total_tax for order in orders)}",
                "total_surcharge": f"{sum(order.total_surcharge for order in orders)}"}
# f"orders__during_{target_year}-{target_month}": orders

    return {"warehouse": f"{warehouse_id}",
            "target_month": f"{target_year}-{target_month}",
            "orders_done": f"{len(orders)}",
            "amount_of_items_sold": f"{items_totaal}",
            "total_revenue": f"{sum(order.total_amount for order in orders)}",
            "total_discount": f"{sum(order.total_discount for order in orders)}",
            "total_tax": f"{sum(order.total_tax for order in orders)}",
            "total_surcharge": f"{sum(order.total_surcharge for order in orders)}"}
# f"orders_for_warehouse-{warehouse_id}_during_{target_year}-{target_month}": orders


def general_report(db: Session, target_year: int, target_month: int, offset: int, limit: int):
    orders = (
              db.query(Order)
              .filter(extract('year', Order.order_date) == target_year)
              .filter(extract('month', Order.order_date) == target_month)
              .offset(offset)
              .limit(limit)
              .all()
              )

    return reporter(target_year, target_month, orders)


def report_for_warehouse(db: Session, warehouse_id: int, target_year: int, target_month: int):
    orders = (
              db.query(Order)
              .filter(Order.warehouse_id == warehouse_id)
              .filter(extract('year', Order.order_date) == target_year)
              .filter(extract('month', Order.order_date) == target_month)
              .all()
              )

    return reporter(target_year, target_month, orders, warehouse_id)
