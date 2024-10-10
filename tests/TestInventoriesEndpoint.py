import unittest
from httpx import Client


class testInventoriesEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/inventories"
        self.client = Client()
        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}
        self.data = {"id": 11721, "item_id": "0000000000000", "description": "Down-sized system-worthy productivity", "item_reference": "mYt79640E", "locations": [30113, 30437, 9010, 11731, 25614, 25515, 4192, 19302, 3946, 26883, 9308, 22330, 14470, 8871, 8326, 18266, 17880, 33186, 33547], "total_on_hand": 334, "total_expected": 0, "total_ordered": 304, "total_allocated": 77, "total_available": -47, "created_at": "1997-05-13 02:30:31", "updated_at": "2003-10-18 00:21:57"}

    def test_get_inventories(self):
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
