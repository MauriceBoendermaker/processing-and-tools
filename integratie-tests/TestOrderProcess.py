import unittest
from httpx import Client
from datetime import date
from test_utils import match_date_timezone, check_id_exists


class TestOrderResource(unittest.TestCase):
    def setUp(self):
        self.ordersUrl = "http://localhost:3000/api/v2/orders/"
        self.inventoriesUrl = "http://localhost:3000/api/v2/inventories/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "Content-Type": "application/json"}

        self.ORDER_TEST_ID = 13348

        self.TEST_BODY = {
            "id": self.ORDER_TEST_ID,
            "source_id": 82,
            "order_date": "1995-05-27T20:02:30Z",
            "request_date": "1995-05-31T20:02:30Z",
            "reference": "ORD06490",
            "reference_extra": "Lorem ipsum dolor sit amet.",
            "order_status": "Invalid Field",
            "notes": "Lorem ipsum dolor sit amet.",
            "shipping_notes": "Lorem ipsum dolor sit amet.",
            "picking_notes": "Lorem ipsum dolor sit amet.",
            "warehouse_id": 36,
            "ship_to": 5254,
            "bill_to": 3016,
            "shipment_id": [5555],
            "total_amount": 6070.46,
            "total_discount": 295.5,
            "total_tax": 388.58,
            "total_surcharge": 37.91,
            "created_at": "1995-05-27T20:02:30Z",
            "updated_at": "1995-05-29T16:02:30Z",
            "is_deleted": False,
            "items": [
                {
                    "item_id": "P008386",
                    "amount": 7
                }
            ]
        }

        self.ToPut = {
            "notes": "UPDATED TEKST.",
            "shipping_notes": "UPDATED TEKST.",
            "picking_notes": "UPDATED TEKST."
        }

    def test_1_order_input_validation(self):
        response = self.client.post(self.ordersUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 422)
        print(response.json())

    def test_2_invalid_stock(self):
        response = self.client.get(f"{self.inventoriesUrl}1")
        inven = response.json()

        order_body = self.TEST_BODY
        available = inven["total_available"]
        order_body["items"] = [{"item_id": f"{inven['item_id']}", "amount": available + 1}]

        response = self.client.post(self.ordersUrl, json=order_body)

        self.assertEqual(response.status_code, 409)
        self.assertIn(f"only {available} available", response.json().get("detail"))


if __name__ == '__main__':
    unittest.main()
