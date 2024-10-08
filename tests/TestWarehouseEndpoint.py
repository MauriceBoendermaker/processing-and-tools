import unittest
from httpx import Client


class TestWarehouseEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/warehouses"
        self.client = Client()
        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}
        self.data = {"id": "test"}

    def test_get_warehouses(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)

    def test_post_warehouse(self):
        response = self.client.post(self.baseUrl, json=self.data)

        self.assertEqual(response.status_code, 201)

    def test_get_warehouse(self):
        response = self.client.get(f"{self.baseUrl}/1")

        self.assertEqual(response.status_code, 200)

    def test_delete_warehouse(self):
        response = self.client.delete(self.baseUrl + "/57")

        self.assertEqual(response.status_code, 200)

    def test_put_warehouse(self):
        response = self.client.put(
            self.baseUrl + "/1", json=self.client.get(f"{self.baseUrl}/1").json())

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
