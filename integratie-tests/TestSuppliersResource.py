import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists, check_code_exists


class TestSupplierResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/suppliers/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "Content-Type": "application/json"}

        self.TEST_ID = 498
        self.TEST_ID_ITEMS = 100  # Only the first 100 suppliers have items

        self.TEST_BODY = {
            "id": self.TEST_ID,
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
            "name": "Test Name"
        }

    def test_1_post_supplier(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [200, 201])

    def test_2_get_suppliers(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), 100)

    def test_3_get_supplier(self):
        response = self.client.get(f"{self.baseUrl}?code=SUP0498")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), self.TEST_BODY["id"])
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("name"), self.TEST_BODY["name"])
        self.assertEqual(body.get("city"), self.TEST_BODY["city"])
        self.assertEqual(body.get("zip_code"), self.TEST_BODY["zip_code"])
        self.assertEqual(body.get("province"), self.TEST_BODY["province"])
        self.assertEqual(body.get("country"), self.TEST_BODY["country"])
        self.assertEqual(body.get("contact_name"), self.TEST_BODY["contact_name"])
        self.assertTrue(match_date(body.get("created_at"), date.today()))

    """
    def test_4_get_supplier_items(self):
        response = self.client.get(f"{self.baseUrl}100/items")
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
        self.assertEqual(first_item.get("supplier_id"), self.TEST_ID_ITEMS)
        self.assertEqual(first_item.get("supplier_code"), "SUP347")
    """
    def test_5_put_supplier(self):
        response = self.client.put(f"{self.baseUrl}{self.TEST_BODY["code"]}", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?code={self.TEST_BODY["code"]}")
        body = response.json()

        self.assertEqual(body.get("name"), self.ToPut["name"])
        self.assertTrue(match_date(body.get("updated_at"), date.today()))

    def test_6_delete_supplier(self):
        response = self.client.delete(f"{self.baseUrl}{self.TEST_BODY["code"]}")

        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.baseUrl)
        print(f"Check if id {self.TEST_ID} is deleted: ")
        self.assertFalse(check_code_exists(response.json(), self.TEST_BODY["code"]))

    def test_7_no_apikey(self):
        self.client.headers = {"Content-Type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 422)

    def test_7_wrong_apikey(self):
        self.client.headers = {"api-key": "onzin", "Content-Type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
