import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists, check_reference_exists


class TestInventoriesEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/inventories/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "Content-Type": "application/json"}

        self.TEST_ID = 11721

        self.TEST_BODY = {
            "id": self.TEST_ID,
            "item_id": "P000000",
            "description": "Down-sized system-worthy productivity",
            "item_reference": "tijdelijke-item",
            "total_on_hand": 334,
            "total_expected": 0,
            "total_ordered": 304,
            "total_allocated": 77,
            "total_available": -47,
            "locations": [
                        30113, 30437, 9010, 11731,
                        25614, 25515, 4192, 19302, 3946,
                        26883, 9308, 22330, 14470, 8871,
                        8326, 18266, 17880, 33186, 33547],
            "is_deleted": False
        }

        self.ToPut = {
            "description": "Updated description",
            "total_on_hand": 450,
            "total_expected": 1,
            "total_ordered": 70
        }

        self.NEW_ITEM = {
            "uid": "P000000",
            "code": "tijdelijke-item",
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

    def test_1_post_inventory(self):
        # Add the test inventory to be used in tests
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [200, 201])
        self.assertIn("tijdelijke-item", response.json().get("item_reference"))

    def test_2_get_inventories(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), 100)

    def test_3_get_inventory(self):
        response = self.client.get(f"{self.baseUrl}?item_reference=P000000")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        print(body)
        self.assertEqual(body.get("item_reference"), "tijdelijke-item")
        self.assertEqual(body.get("description"),
                         self.TEST_BODY["description"])
        self.assertTrue(match_date(body.get("created_at"), date.today()))

    def test_4_put_inventory(self):
        response = self.client.put(
            f"{self.baseUrl}P000000", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        # Verify update worked
        body = response.json()
        self.assertEqual(body.get("total_expected"), self.ToPut["total_expected"])
        self.assertEqual(body.get("description"), self.ToPut["description"])
        self.assertEqual(body.get("total_on_hand"),
                         self.ToPut["total_on_hand"])
        self.assertEqual(body.get("total_ordered"),
                         self.ToPut["total_ordered"])
        self.assertTrue(match_date(body.get("updated_at"), date.today()))

    def test_5_get_locations(self):
        response = self.client.get(
            f"{self.baseUrl}P000000/locations", json=self.ToPut)
        self.assertEqual(response.status_code, 200)
        self.assertIn(30113, response.json())

    def test_6_delete_inventory(self):
        # cleanup/teardown
        response = self.client.delete(f"{self.baseUrl}P000000")

        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = self.client.get(self.baseUrl)
        self.assertFalse(check_reference_exists(response.json(), "tijdelijke-item"))

    def test_7_no_key(self):
        self.client.headers = {"Content-Type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 422)

    def test_8_wrong_key(self):
        self.client.headers = {"api-key": "poging", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
