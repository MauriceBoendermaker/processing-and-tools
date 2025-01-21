import unittest
from httpx import Client
from test_utils import check_id_exists, match_date
from datetime import datetime


class TestLocationsResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/locations/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 34534
        self.TEST_BODY = {
            "id": self.TEST_ID,
            "warehouse_id": 58,
            "code": "A.1.0",
            "name": "Row: A, Rack: 1, Shelf: 0",
            "is_deleted": False,
            "max_weight": 100000.50,
            "stock": [{"empty": 0}]
        }

        self.ToPut = {
            "name": "Updated Row: A, Rack: 1, Shelf: 0"
        }

    # Test to create a location using POST
    def test_1_post_location(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [200, 201])
        body = response.json()
        self.assertEqual(body["code"], self.TEST_BODY["code"])
        self.assertEqual(body["name"], self.TEST_BODY["name"])

    # Test to get all locations using GET
    def test_2_get_locations(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(isinstance(body, list))
        self.assertTrue(len(body) == 100)

    # Test to get a single location by ID using GET
    def test_3_get_location_by_id(self):
        response = self.client.get(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["id"], self.TEST_ID)
        self.assertEqual(body["code"], self.TEST_BODY["code"])
        self.assertEqual(body["name"], self.TEST_BODY["name"])

    # Test to get locations by warehouse ID using GET
    def test_4_get_locations_by_warehouse(self):
        response = self.client.get(f"{self.baseUrl}warehouse/{self.TEST_BODY['warehouse_id']}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(isinstance(body, list))
        self.assertTrue(any(loc["warehouse_id"] == self.TEST_BODY["warehouse_id"] for loc in body))

    # Test to update a location using PUT
    def test_5_put_location(self):
        response = self.client.put(f"{self.baseUrl}{self.TEST_ID}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["name"], self.ToPut["name"])
        self.assertTrue(match_date(body["updated_at"], datetime.today().date()))

    def test_6_delete_location(self):
        # Perform DELETE request
        response = self.client.delete(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["detail"], "Location soft deleted")

        # Verify the location is no longer accessible
        response = self.client.get(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 404)


    # Test unauthorized access by removing the API key
    def test_7_nokey(self):
        self.client.headers = {"content-type": "application/json"}  # Remove API key
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    # Test with an incorrect API key
    def test_8_wrong_key(self):
        self.client.headers = {"api-key": "invalid-key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
