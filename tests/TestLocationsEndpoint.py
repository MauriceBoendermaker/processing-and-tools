import unittest
from httpx import Client
from test_utils import match_date, check_id_exists
from datetime import date

class TestLocationResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/locations"
        self.client = Client()

        self.test_body = {
            "id": 1,
            "warehouse_id": 1,
            "code": "A.1.0",
            "name": "Row: A, Rack: 1, Shelf: 0",
            "created_at": "2024-10-14 12:00:00",
            "updated_at": "2024-10-14 12:00:00"
        }

        self.ToPut = {
            "id": 1,
            "warehouse_id": 1,
            "code": "A.1.0",
            "name": "Updated Row: A, Rack: 1, Shelf: 0",
            "created_at": "2024-10-14 12:00:00",
            "updated_at": "2024-10-14 12:00:00"
        }

        self.client.headers = {"API_KEY": "a1b2c3d4e5", "content-type": "application/json"}

    # Test to create a location using POST
    def test_1_post_location(self):
        response = self.client.post(self.baseUrl, json=self.test_body)
        self.assertEqual(response.status_code, 201)

    # Test to get all locations using GET
    def test_2_get_locations(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_id_exists(body, 1))

    # Test to get a single location by ID using GET
    def test_3_get_location_by_id(self):
        response = self.client.get(f"{self.baseUrl}/1")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("id"), 1)
        self.assertEqual(body.get("code"), "A.1.0")
        self.assertEqual(body.get("name"), "Row: A, Rack: 1, Shelf: 0")

    # Test to update a location using PUT
    def test_4_put_location(self):
        response = self.client.put(f"{self.baseUrl}/1", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Fetch the updated location
        response = self.client.get(f"{self.baseUrl}/1")
        body = response.json()
        self.assertEqual(body.get("name"), "Updated Row: A, Rack: 1, Shelf: 0")
        self.assertTrue(match_date(body.get('updated_at'), date.today()))

    # Test to delete a location using DELETE
    def test_5_delete_location(self):
        response = self.client.delete(f"{self.baseUrl}/1")
        self.assertEqual(response.status_code, 200)

        # Verify it was deleted
        response = self.client.get(self.baseUrl)
        self.assertFalse(check_id_exists(response.json(), 1))

    # Test unauthorized access by removing the API key
    def test_6_unauthorized(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
