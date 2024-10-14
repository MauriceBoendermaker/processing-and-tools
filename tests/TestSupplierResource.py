import unittest
from httpx import Client
from test_utils import match_date, check_id_exists
from datetime import date

class TestSupplierResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/suppliers"
        self.client = Client()

        self.test_id = 498
        self.test_id_items = 100  # Only the first 100 suppliers have items

        self.test_body = {
            "id": self.test_id,
            "code": "SUP0498",
            "name": "Neal-Hoffman",
            "address": "7032 Mindy Meadow",
            "address_extra": "Apt. 937",
            "city": "Lake Alex",
            "zip_code": "62913",
            "province": "Washington",
            "country": "Taiwan",
            "contact_name": "Jeffrey Larsen",
            "phonenumber": "(786)666-7146",
            "reference": "N-SUP0498",
            "created_at": "1987-06-10 04:33:51",
            "updated_at": "2014-06-24 16:12:58"
        }

        self.ToPut = {
            "id": self.test_id,
            "code": "SUP0498",
            "name": "Test Name",
            "address": "7032 Mindy Meadow",
            "address_extra": "Apt. 001",
            "city": "Rotterdam",
            "zip_code": "42069",
            "province": "New Amsterdam",
            "country": "Congo",
            "contact_name": "Jeffrey Epstein",
            "phonenumber": "(786)666-7146",
            "reference": "N-SUP0498",
            "created_at": "1987-06-10 04:33:51",
            "updated_at": "2014-06-24 16:12:58"
        }

        self.client.headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

    def test_1_post_supplier(self):
        response = self.client.post(self.baseUrl, json=self.test_body)
        if response.status_code not in [200, 201]:
            print(f"Failed to add supplier: {response.status_code}, {response.text}")

    def test_2_get_suppliers(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_id_exists(body, self.test_id))

    def test_3_get_supplier(self):
        response = self.client.get(f"{self.baseUrl}/{self.test_id}")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), self.test_body["id"])
        self.assertEqual(body.get("code"), self.test_body["code"])
        self.assertEqual(body.get("name"), self.test_body["name"])
        self.assertEqual(body.get("city"), self.test_body["city"])
        self.assertEqual(body.get("zip_code"), self.test_body["zip_code"])
        self.assertEqual(body.get("province"), self.test_body["province"])
        self.assertEqual(body.get("country"), self.test_body["country"])
        self.assertEqual(body.get("contact_name"), self.test_body["contact_name"])
        self.assertTrue(match_date(body.get("created_at"), date.today()))

    def test_4_get_supplier_items(self):
        response = self.client.get(f"{self.baseUrl}/{self.test_id_items}/items")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(body, list)
        self.assertGreater(len(body), 0)

        first_item = body[0]
        self.assertEqual(first_item.get("uid"), "P000012")
        self.assertEqual(first_item.get("code"), "USN48902j")
        self.assertEqual(first_item.get("description"), "Right-sized discrete website")
        self.assertEqual(first_item.get("short_description"), "stand")
        self.assertEqual(first_item.get("item_line"), 50)
        self.assertEqual(first_item.get("item_group"), 41)
        self.assertEqual(first_item.get("item_type"), 95)
        self.assertEqual(first_item.get("pack_order_quantity"), 6)
        self.assertEqual(first_item.get("supplier_id"), self.test_id_items)
        self.assertEqual(first_item.get("supplier_code"), "SUP347")

if __name__ == '__main__':
    unittest.main()
