import unittest
from httpx import Client


class TestWarehouseEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/warehouses"
        self.client = Client()

    def test_get_warehouses(self):
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), )


if __name__ == '__main__':
    unittest.main()
