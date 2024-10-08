import unittest
from httpx import Client

class testLocationsEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/locations/23"
        self.client = Client()
        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}
        self.data = {  "id": 23, "warehouse_id": 1, "code": "A.8.0", "name": "Row: A, Rack: 8, Shelf: 0", "created_at": "1992-05-15 03:21:32", "updated_at": "1992-05-15 03:21:32"}

    def test_get_locations(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)

    def test_post_inventories(self):
        response = self.client.post(self.baseUrl, json=self.data)
        self.assertEqual(response.status_code, 201)

    def test_get_inventories(self):
        response = self.client.get(f"{self.baseUrl}/58")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
