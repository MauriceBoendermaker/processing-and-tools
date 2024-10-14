import unittest
from httpx import Client
from test_utils import match_date, check_id_exists
from datetime import date


class TestItemLinesResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/item_lines"
        self.client = Client()

        self.test_body = {
            "id": 97,
            "name": "New Gadget Line",
            "description": "Latest gadget releases",
            "created_at": "2024-10-14 12:00:00",
            "updated_at": "2024-10-14 12:00:00"
        }

        self.ToPut = {
            "id": 95,
            "name": "Updated Gadget Line",
            "description": "Updated gadget releases",
            "created_at": "2024-10-14 12:00:00",
            "updated_at": "2024-10-14 12:00:00"
        }

        self.original = {"id": 95, "name": "Exhibition Equipment", "description": "",
                         "created_at": "2024-07-26 06:18:08", "updated_at": "2024-08-09 18:49:42"}

        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}

    # POST is niet mogelijk voor item_lines
    def test_1_post_item_line(self):
        response = self.client.post(self.baseUrl, json=self.test_body)
        self.assertEqual(response.status_code, 404)

    # Test to get all item lines using GET
    def test_2_get_item_lines(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        # Check laatste ID 95
        self.assertTrue(check_id_exists(body, 95))

    # Test to get a single item line by ID using GET
    def test_3_get_item_line_by_id(self):
        response = self.client.get(f"{self.baseUrl}/95")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("id"), 95)
        self.assertEqual(body.get("name"), "Exhibition Equipment")
        self.assertEqual(body.get("description"), "")

    # Test to update an item line using PUT
    def test_4_put_item_line(self):
        response = self.client.put(f"{self.baseUrl}/95", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Fetch the updated item line
        response = self.client.get(f"{self.baseUrl}/95")
        body = response.json()
        self.assertEqual(body.get("name"), "Updated Gadget Line")
        self.assertEqual(body.get("description"), "Updated gadget releases")
        self.assertTrue(match_date(body.get('updated_at'), date.today()))

        self.client.put(f"{self.baseUrl}/95", json=self.original)

    # Test to delete an item line using DELETE
    def test_5_delete_item_line(self):
        response = self.client.delete(f"{self.baseUrl}/97")
        self.assertEqual(response.status_code, 200)

        # Verify it was deleted
        response = self.client.get(self.baseUrl)
        self.assertFalse(check_id_exists(response.json(), 97))

    # Test unauthorized access by removing the API key
    def test_6_unauthorized(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
