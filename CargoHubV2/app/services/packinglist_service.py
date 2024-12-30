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

TEMPLATE_FILE = Path(os.path.dirname(__file__)).parent / "packinglist_template.html"


def generate_packing_list(order: Order):
    try:
        # Parse the items data from the order
        try:
            items = json.loads(order.items) if isinstance(order.items, str) else order.items
            if not isinstance(items, list):
                raise ValueError("Items should be a list of dictionaries with 'item_id' and 'amount'.")
        except json.JSONDecodeError:
            raise ValueError("Failed to decode order items. Ensure items are in valid JSON format.")
        

        total_amount = sum(item["amount"] for item in items)
        
        # Prepare data for the packing list
        content = {
            "warehouse_id": order.warehouse_id,
            "source_id": order.source_id,
            "shipping_notes": order.shipping_notes,
            "order_date": order.order_date.strftime("%Y-%m-%d"),
            "order_id": order.id,
            "request_date": order.request_date.strftime("%Y-%m-%d"),
            "total_items": len(items),
            "total_amount": total_amount,
            "items": [{"item_id": item["item_id"], "amount": item["amount"]} for item in items],  # Simplified item list
        }

        # Load the packing list template
        with open(TEMPLATE_FILE, "r") as file:
            html_template = file.read()

        # Render the template
        template = Template(html_template)
        html_content = template.render(**content)

        # Define PDF file path
        pdf_filename = f"packinglist_order_{order.id}.pdf"
        pdf_path = PDF_DIR / pdf_filename

        # Generate PDF
        pdfkit.from_string(html_content, str(pdf_path))

        # Return the file URL or file path
        pdf_url = f"http://127.0.0.1:3000/api/v2/packinglist/get-pdf/{pdf_filename}"
        return JSONResponse({"message": "Packing list PDF generated successfully.", "pdf_url": pdf_url})
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating packing list PDF, {e}")
