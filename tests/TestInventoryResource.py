import unittest
from httpx import Client
from test_utils import match_date_inventories, check_id_exists
from datetime import date


class TestInventoriesEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/inventories"
        self.client = Client()

        self.test_id = 11719

        self.test_body = {
            "id": self.test_id,
            "item_id": "0000000000000",
            "description": "Down-sized system-worthy productivity",
            "item_reference": "mYt79640E",
            "locations": [
                30113, 30437, 9010, 11731, 25614, 25515, 4192, 19302, 3946,
                26883, 9308, 22330, 14470, 8871, 8326, 18266, 17880, 33186, 33547
            ],
            "total_on_hand": 334,
            "total_expected": 0,
            "total_ordered": 304,
            "total_allocated": 77,
            "total_available": -47,
            "created_at": "2024-01-01 12:00:00",
            "updated_at": "2024-01-01 12:00:00"
        }

        self.ToPut = {
            "id": self.test_id,
            "item_id": "0000000000000",
            "description": "Updated description",
            "item_reference": "mYt79640E",
            "locations": [
                30113, 30437, 9010, 11731, 25614, 25515, 4192, 19302, 3946,
                26883, 9308, 22330, 14470, 8871, 8326, 18266, 17880, 33186, 33547
            ],
            "total_on_hand": 420,
            "total_expected": 0,
            "total_ordered": 69,
            "total_allocated": 77,
            "total_available": -47,
            "created_at": "2024-01-01 12:00:00",
            "updated_at": "2024-01-02 12:00:00"
        }

        self.client.headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        # Clean up any existing inventory with the same ID to avoid duplicates
        self.client.delete(f"{self.baseUrl}/{self.test_id}")

        # Add the test inventory to be used in tests
        response = self.client.post(self.baseUrl, json=self.test_body)
        if response.status_code not in [200, 201]:
            print(f"Setup failed to add inventory: {response.status_code}, {response.text}")

    def tearDown(self):
        # Clean up the test inventory after each test
        response = self.client.delete(f"{self.baseUrl}/{self.test_id}")
        if response.status_code not in [200, 404]:
            print(f"TearDown failed to delete inventory: {response.status_code}, {response.text}")

    def test_2_get_inventories(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        print("Response for test_2_get_inventories:", body)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_id_exists(body, self.test_id))

    def test_3_get_inventory(self):
        response = self.client.get(f"{self.baseUrl}/{self.test_id}")
        print("Response status code for test_3_get_inventory:", response.status_code)
        print("Response body for test_3_get_inventory:", response.text)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), self.test_body["id"])
        self.assertEqual(body.get("item_id"), self.test_body["item_id"])
        self.assertEqual(body.get("description"), self.test_body["description"])
        self.assertTrue(match_date_inventories(body.get("created_at"), date(2024, 1, 1)))

    def test_4_put_inventory(self):
        response = self.client.put(f"{self.baseUrl}/{self.test_id}", json=self.ToPut)
        print("Response status code for test_4_put_inventory:", response.status_code)
        print("Response body for test_4_put_inventory:", response.text)

        self.assertEqual(response.status_code, 200)

        # Verify update worked
        response = self.client.get(f"{self.baseUrl}/{self.test_id}")
        body = response.json()
        self.assertEqual(body.get("id"), self.ToPut["id"])
        self.assertEqual(body.get("description"), self.ToPut["description"])
        self.assertEqual(body.get("total_on_hand"), self.ToPut["total_on_hand"])
        self.assertTrue(match_date_inventories(body.get("updated_at"), date(2024, 1, 2)))

    def test_5_get_inventory_locations(self):
        response = self.client.get(f"{self.baseUrl}/{self.test_id}/locations")
        print("Response for test_5_get_inventory_locations:", response.text)

        self.assertEqual(response.status_code, 200)

        body = response.json()
        if len(body) < 2:  # To avoid index out of range
            print("Locations not found in response.")
        else:
            self.assertEqual(body[0], self.test_body["locations"][0])
            self.assertEqual(body[1], self.test_body["locations"][1])

    def test_6_delete_inventory(self):
        response = self.client.delete(f"{self.baseUrl}/{self.test_id}")
        print("Response status code for test_6_delete_inventory:", response.status_code)
        print("Response body for test_6_delete_inventory:", response.text)

        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = self.client.get(f"{self.baseUrl}/{self.test_id}")
        print("Response status code for deleted inventory check:", response.status_code)
        self.assertEqual(response.status_code, 404)

    def test_7_unauthorized(self):
        self.client.headers = {"Content-Type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
