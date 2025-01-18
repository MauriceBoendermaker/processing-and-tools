import unittest
from httpx import Client
from datetime import date
from test_utils import match_date_timezone, check_id_exists


class TestOrderResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/orders/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5",
                               "Content-Type": "application/json"}

        self.TEST_ID = 13354

        self.TEST_BODY = {
            "id": self.TEST_ID,
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
            "shipment_id": [8737],
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
            "notes": "UPDATED.",
            "shipping_notes": "UPDATED.",
            "picking_notes": "UPDATED."
        }

    def test_1_post_order(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [200, 201])

    def test_2_get_orders(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(check_id_exists(body, self.TEST_ID))

    def test_3_get_order(self):
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), self.TEST_BODY["id"])
        self.assertEqual(body.get("source_id"), self.TEST_BODY["source_id"])
        self.assertEqual(body.get("reference"), self.TEST_BODY["reference"])
        self.assertEqual(body.get("order_status"),
                         self.TEST_BODY["order_status"])
        self.assertEqual(body.get("notes"), self.TEST_BODY["notes"])
        self.assertEqual(body.get("ship_to"), self.TEST_BODY["ship_to"])
        self.assertEqual(body.get("bill_to"), self.TEST_BODY["bill_to"])
        self.assertEqual(body.get("total_surcharge"),
                         self.TEST_BODY["total_surcharge"])
        # self.assertTrue(match_date_timezone(body.get("created_at"), date.today()))

    def test_4_get_order_items(self):

        response = self.client.get(f"{self.baseUrl}{self.TEST_ID}/items")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body[0].get("item_id"),
                         self.TEST_BODY["items"][0]["item_id"])
        self.assertEqual(body[0].get("amount"),
                         self.TEST_BODY["items"][0]["amount"])

    def test_5_put_order(self):
        response = self.client.put(
            f"{self.baseUrl}{self.TEST_ID}", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()

        self.assertEqual(body.get("notes"), self.ToPut["notes"])
        self.assertEqual(body.get("shipping_notes"),
                         self.ToPut["shipping_notes"])
        self.assertEqual(body.get("picking_notes"),
                         self.ToPut["picking_notes"])
        # self.assertTrue(match_date_timezone(body.get("updated_at"), date.today()))

    def test_7_no_apikey(self):
        self.client.headers = {"Content-Type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 422)

    def test_8_get_orders_sorted_asc(self):
        # Ensure the order exists before testing
        # self.client.post(self.baseUrl, json=self.TEST_BODY)

        response = self.client.get(f"{self.baseUrl}?sort_order=asc")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        dates = [order["order_date"] for order in body]
        self.assertEqual(dates, sorted(dates))

    def test_9_get_orders_sorted_desc(self):
        # Ensure the order exists before testing
        # self.client.post(self.baseUrl, json=self.TEST_BODY)

        response = self.client.get(f"{self.baseUrl}?sort_order=desc")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        dates = [order["order_date"] for order in body]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test__10_delete_order(self):
        # Ensure the order exists before testing
        # self.client.post(self.baseUrl, json=self.TEST_BODY)

        response = self.client.delete(f"{self.baseUrl}{self.TEST_ID}")

        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.baseUrl)
        print(f"Check if id {self.TEST_ID} is deleted: ")
        self.assertFalse(check_id_exists(response.json(), self.TEST_ID))


if __name__ == '__main__':
    unittest.main()
