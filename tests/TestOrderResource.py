import unittest
from httpx import Client
from test_utils import match_date, check_id_exists
from datetime import date

class TestOrderResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/orders"
        self.client = Client()

        self.test_id = 6490

        self.test_body = {
            "id": self.test_id,
            "source_id": 82,
            "order_date": "1995-05-27T20:02:30Z",
            "request_date": "1995-05-31T20:02:30Z",
            "reference": "ORD06490",
            "reference_extra": "Lorem ipsum dolor sit amet.",
            "order_status": "Pending",
            "notes": "Lorem ipsum dolor sit amet.",
            "shipping_notes": "Lorem ipsum dolor sit amet.",
            "picking_notes": "Lorem ipsum dolor sit amet.",
            "warehouse_id": 36,
            "ship_to": 5254,
            "bill_to": 3016,
            "shipment_id": 5555,
            "total_amount": 6070.46,
            "total_discount": 295.5,
            "total_tax": 388.58,
            "total_surcharge": 37.91,
            "created_at": "1995-05-27T20:02:30Z",
            "updated_at": "1995-05-29T16:02:30Z",
            "items": [
                {
                    "item_id": "P008386",
                    "amount": 7
                }
            ]
        }

        self.ToPut = {
            "id": self.test_id,
            "source_id": 69,
            "order_date": "1995-05-27T20:02:30Z",
            "request_date": "1995-05-31T20:02:30Z",
            "reference": "ORD06490",
            "reference_extra": "UPDATED TEKST.",
            "order_status": "Pending",
            "notes": "UPDATED TEKST.",
            "shipping_notes": "UPDATED TEKST.",
            "picking_notes": "UPDATED TEKST.",
            "warehouse_id": 36,
            "ship_to": 5254,
            "bill_to": 3016,
            "shipment_id": 6666,
            "total_amount": 6070.46,
            "total_discount": 295.5,
            "total_tax": 388.58,
            "total_surcharge": 37.91,
            "created_at": "1995-05-27T20:02:30Z",
            "updated_at": "1995-05-29T16:02:30Z",
            "items": [
                {
                    "item_id": "P008386",
                    "amount": 7
                }
            ]
        }

        self.client.headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

if __name__ == '__main__':
    unittest.main()
