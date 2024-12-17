import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists


class TestShipmentResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/shipments/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5",
                               "content-type": "application/json"}

        self.TEST_ID = 10103

        self.test_body = {
            "id": self.TEST_ID,
            "order_id": [6488],
            "source_id": 36,
            "order_date": "2007-08-08",
            "request_date": "2007-08-10",
            "shipment_date": "2007-08-12",
            "shipment_type": "O",
            "shipment_status": "Pending",
            "notes": "Ei fel god.",
            "carrier_code": "FedEx",
            "carrier_description": "Federal Express",
            "service_code": "Fastest",
            "payment_type": "Manual",
            "transfer_mode": "Ground",
            "total_package_count": 3,
            "total_package_weight": 480.53,
            "created_at": "2007-08-09T05:51:11Z",
            "updated_at": "2007-08-10T07:51:11Z",
            "is_deleted": False,
            "items": [
                {
                    "item_id": "P006938",
                    "amount": 42
                },
                {
                    "item_id": "P006934",
                    "amount": 25
                },
                {
                    "item_id": "P010624",
                    "amount": 23
                },
                {
                    "item_id": "P008658",
                    "amount": 33
                },
                {
                    "item_id": "P003438",
                    "amount": 37
                },
                {
                    "item_id": "P003598",
                    "amount": 40
                },
                {
                    "item_id": "P002020",
                    "amount": 13
                },
                {
                    "item_id": "P007158",
                    "amount": 32
                },
                {
                    "item_id": "P007575",
                    "amount": 5
                },
                {
                    "item_id": "P001698",
                    "amount": 9
                },
                {
                    "item_id": "P002366",
                    "amount": 18
                },
                {
                    "item_id": "P000129",
                    "amount": 38
                },
                {
                    "item_id": "P004158",
                    "amount": 5
                },
                {
                    "item_id": "P001385",
                    "amount": 26
                }
            ]
        }

        self.ToPut = {
            "notes": "AANGEPAST"
        }

    # genummerd omdat volgorde van executie alfabetisch gaat
    def test_1_post_shipment(self):
        response = self.client.post(self.baseUrl, json=self.test_body)

        self.assertIn(response.status_code, [201, 200])

        # in de toekomst moet POST ook body teruggeven met gemaakte resource:
        # self.assertEqual(response.json().get("notes"), "self.test_body["notes"]")

    def test_2_get_shipments(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(check_id_exists(body, self.TEST_ID))

    def test_3_get_shipment(self):
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        # check of body klopt
        self.assertEqual(body.get("id"), self.test_body["id"])
        self.assertEqual(body.get("order_id"), self.test_body["order_id"])
        self.assertEqual(body.get("source_id"), self.test_body["source_id"])
        self.assertEqual(body.get("notes"), self.test_body["notes"])
        self.assertEqual(body.get("carrier_code"),
                         self.test_body["carrier_code"])

    def test_4_put_shipment(self):
        response = self.client.put(
            f"{self.baseUrl}{self.TEST_ID}", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()

        self.assertEqual(body.get("notes"), self.ToPut["notes"])
        # self.assertTrue(match_date(body.get('updated_at'), date.today()))

    """
    def test_5_get_shipment_items(self):
        # krijgt een lijst met item_ids en amounts terug (2 Kvps)
        response = self.client.get(f"{self.baseUrl}/{self.TEST_ID}/items")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body[0].get("item_id"),
                         self.test_body["items"][0]["item_id"])
        self.assertEqual(body[0].get("amount"),
                         self.test_body["items"][0]["amount"])
        self.assertEqual(body[1].get("item_id"),
                         self.test_body["items"][1]["item_id"])
        self.assertEqual(body[1].get("amount"),
                         self.test_body["items"][1]["amount"])
    """

    def test_6_delete_shipment(self):
        # teardown/cleanup
        response = self.client.delete(f"{self.baseUrl}{self.TEST_ID}")

        self.assertEqual(response.status_code, 200)

        na_delete = self.client.get(self.baseUrl)
        # check of deleted
        self.assertFalse(check_id_exists(na_delete.json(), self.TEST_ID))

    """
    def test_7_get_shipment_orders(self):
        # krijgt een lijst met order_ids terug die deze shipment id hebben
        response = self.client.get(f"{self.baseUrl}1/orders")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(body[0], int))
    """

    def test_8_no_apikey(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 422)

    def test_8_wrong_apikey(self):
        self.client.headers = {"api-key": "something",
                               "content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
