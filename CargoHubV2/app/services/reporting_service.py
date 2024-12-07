from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import extract
from CargoHubV2.app.models.orders_model import Order


def reporter(
        target_year: int,
        target_month: int,
        orders: list[Order],
        warehouse_id: int = 0):
    if warehouse_id == 0:
        return {"target_month": f"{target_year}/{target_month}",
                "orders_done": len(orders),
                "amount_of_items_sold": sum(item['amount'] for order in orders for item in order.items),
                "total_revenue": sum(order.total_amount for order in orders),
                "total_discount": sum(order.total_discount for order in orders),
                "total_tax": sum(order.total_tax for order in orders),
                "total_surcharge": sum(order.total_surcharge for order in orders),
                f"orders__during_{target_year}/{target_month}": orders}

    return {"warehouse": warehouse_id,
            "target_month": f"{target_year}/{target_month}",
            "orders_done": len(orders),
            "amount_of_items_sold": sum(item['amount'] for order in orders for item in order.items),
            "total_revenue": sum(order.total_amount for order in orders),
            "total_discount": sum(order.total_discount for order in orders),
            "total_tax": sum(order.total_tax for order in orders),
            "total_surcharge": sum(order.total_surcharge for order in orders),
            f"orders_for_{warehouse_id}_during_{target_year}/{target_month}": orders}


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
