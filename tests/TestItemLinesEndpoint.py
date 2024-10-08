import unittest
from httpx import Client


class TestItemLinesEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/item_lines"
        self.client = Client()
        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}
        self.data = {"test": "test"}

    def test_get_item_lines(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)


    def test_get_item_line(self):
        response = self.client.get(f"{self.baseUrl}/58")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
