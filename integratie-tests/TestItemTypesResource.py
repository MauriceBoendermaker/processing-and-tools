import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists


class TestItemTypesResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/item_types/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_BODY = {
            "id": 100,
            "name": "Tester",
            "description": "Electronics category",
            "created_at": "2024-10-14 12:00:00",
            "updated_at": "2024-10-14 12:00:00",
            "is_deleted": False

        }

        self.ToPut = {
            "name": "Updated Laptop",
            "description": "Updated electronics category",
        }

        self.original = {"id": 1, "name": "Desktop", "description": "Computers and accessories",
                         "created_at": "2024-07-26 06:18:08", "updated_at": "2024-08-09 18:49:42"}

    # Test to POST a new item type
    def test_1_post_item_type(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [200, 201])

    # Test to get all item types using GET
    def test_2_get_item_types(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        self.assertEqual(response.status_code, 200)

    # Test to get a single item type by ID using GET
    def test_3_get_item_type_by_id(self):
        response = self.client.get(f"{self.baseUrl}?id=100")  # Query parameter for ID
        body = response.json()
        self.assertIn(response.status_code, [200, 201])
        self.assertEqual(body[0].get("id"), 100)  # Response is a list with a single item
        self.assertEqual(body[0].get("name"), self.TEST_BODY["name"])
        self.assertEqual(body[0].get("description"), self.TEST_BODY["description"])

    # Test to update an item type using PUT
    def test_4_put_item_type(self):
        response = self.client.put(f"{self.baseUrl}100", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Fetch the updated item type
        response = self.client.get(f"{self.baseUrl}?id=100")
        body = response.json()
        self.assertEqual(body[0].get("name"), "Updated Laptop")
        self.assertEqual(body[0].get("description"), "Updated electronics category")
        self.assertTrue(match_date(body[0].get('updated_at'), date.today()))

    # Test to delete an item type using DELETE
    def test_5_delete_item_type(self):
        response = self.client.delete(f"{self.baseUrl}100")
        self.assertEqual(response.status_code, 200)

        # Verify it was deleted
        response = self.client.get(self.baseUrl)
        self.assertFalse(check_id_exists(response.json(), 100))

    # Test unauthorized access by removing the API key
    def test_6_no_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    # Test with a wrong API key
    def test_7_wrong_key(self):
        self.client.headers = {"api-key": "nope", "content-type": "application/json"}
        response = self.client.get(self.baseUrl )
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
