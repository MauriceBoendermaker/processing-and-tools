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

    def test_1_post_order(self):
        response = self.client.post(self.baseUrl, json=self.test_body)
        if response.status_code not in [200, 201]:
            print(f"Failed to add order: {response.status_code}, {response.text}")

    def test_2_get_orders(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_id_exists(body, self.test_id))

    def test_3_get_order(self):
        response = self.client.get(f"{self.baseUrl}/{self.test_id}")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), self.test_body["id"])
        self.assertEqual(body.get("source_id"), self.test_body["source_id"])
        self.assertEqual(body.get("reference"), self.test_body["reference"])
        self.assertEqual(body.get("order_status"), self.test_body["order_status"])
        self.assertEqual(body.get("notes"), self.test_body["notes"])
        self.assertEqual(body.get("ship_to"), self.test_body["ship_to"])
        self.assertEqual(body.get("bill_to"), self.test_body["bill_to"])
        self.assertEqual(body.get("total_surcharge"), self.test_body["total_surcharge"])
        self.assertTrue(match_date(body.get("created_at"), date.today()))

    def test_4_get_order_items(self):
        response = self.client.get(f"{self.baseUrl}/{self.test_id}/items")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body[0].get("item_id"),
                         self.ToPut["items"][0]["item_id"])
        self.assertEqual(body[0].get("amount"),
                         self.ToPut["items"][0]["amount"])

    def test_5_put_order(self):
        response = self.client.put(f"{self.baseUrl}/{self.test_id}", json=self.ToPut)
        print("Response status code for test_5_put_order:", response.status_code)
        print("Response body for test_5_put_order", response.text)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}/{self.test_id}")
        body = response.json()

        self.assertEqual(body.get("id"), self.ToPut["id"])
        self.assertEqual(body.get("source_id"), self.ToPut["source_id"])
        self.assertEqual(body.get("reference"), self.ToPut["reference"])
        self.assertEqual(body.get("order_status"), self.ToPut["order_status"])
        self.assertEqual(body.get("notes"), self.ToPut["notes"])
        self.assertEqual(body.get("ship_to"), self.ToPut["ship_to"])
        self.assertEqual(body.get("bill_to"), self.ToPut["bill_to"])
        self.assertEqual(body.get("total_surcharge"), self.ToPut["total_surcharge"])
        self.assertTrue(match_date(body.get("updated_at"), date.today()))

    def test_6_delete_order(self):
        response = self.client.delete(f"{self.baseUrl}/{self.test_id}")
        print("Response status code for test_6_delete_order:", response.status_code)
        print("Response body for test_6_delete_order:", response.text)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.baseUrl)
        print(f"Check if id {self.test_id} is deleted: ")
        self.assertFalse(check_id_exists(response.json(), self.test_id))

    def test_7_unauthorized(self):
        self.client.headers = {"Content-Type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
