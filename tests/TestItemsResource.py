import unittest
from httpx import Client
from test_utils import check_uid_exists
from datetime import date


class TestItemsResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/items"
        self.client = Client()

        self.test_body = {
            "uid": "P000001",
            "code": "sjQ23408K",
            "description": "Face-to-face clear-thinking complexity",
            "short_description": "must",
            "upc_code": "6523540947122",
            "model_number": "63-OFFTq0T",
            "commodity_code": "oTo304",
            "item_line": 11,
            "item_group": 73,
            "item_type": 14,
            "unit_purchase_quantity": 47,
            "unit_order_quantity": 13,
            "pack_order_quantity": 11,
            "supplier_id": 34,
            "supplier_code": "SUP423",
            "supplier_part_number": "E-86805-uTM",
            "created_at": "2015-02-19 16:08:24",
            "updated_at": "2015-09-26 06:37:56"
        }

        self.ToPut = {
            "uid": "P000001",
            "code": "UPD23408K",
            "description": "Updated complexity description",
            "short_description": "updated",
            "upc_code": "6523540947122",
            "model_number": "63-OFFTq0T",
            "commodity_code": "oTo304",
            "item_line": 11,
            "item_group": 73,
            "item_type": 14,
            "unit_purchase_quantity": 47,
            "unit_order_quantity": 13,
            "pack_order_quantity": 11,
            "supplier_id": 34,
            "supplier_code": "SUP423",
            "supplier_part_number": "E-86805-uTM",
            "created_at": "2015-02-19 16:08:24",
            "updated_at": "2015-09-26 06:37:56"
        }

        self.client.headers = {"API_KEY": "a1b2c3d4e5", "content-type": "application/json"}

    # Tests
    def test_1_post_item(self):
        response = self.client.post(self.baseUrl, json=self.test_body)
        self.assertEqual(response.status_code, 201)

    def test_2_get_items(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_uid_exists(body, "P000001"))

    def test_3_get_item(self):
        response = self.client.get(f"{self.baseUrl}/P000001")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("uid"), self.test_body["uid"])
        self.assertEqual(body.get("description"), self.test_body["description"])
        self.assertEqual(body.get("item_group"), self.test_body["item_group"])

    def test_4_put_item(self):
        response = self.client.put(f"{self.baseUrl}/P000001", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}/P000001")
        body = response.json()
        self.assertEqual(body.get("code"), self.ToPut["code"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_5_delete_item(self):
        response = self.client.delete(f"{self.baseUrl}/P000001")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.baseUrl)
        self.assertFalse(check_uid_exists(response.json(), "P000001"))

    def test_6_unauthorized(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
