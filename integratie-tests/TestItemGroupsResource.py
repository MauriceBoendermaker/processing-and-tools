import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists


class TestItemGroupsResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/item_groups/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5",
                               "content-type": "application/json"}

        self.TEST_BODY = {
            "id": 101,
            "name": "Test Group",
            "description": "Group for testing purposes",
            "created_at": "2024-10-14 12:00:00",
            "updated_at": "2024-10-14 12:00:00",
            "is_deleted": False
        }

        self.ToPut = {
            "name": "Updated",
            "description": "Updated",
        }

    # Test to POST a new item group
    def test_1_post_item_group(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [200, 201])

    # Test to GET all item groups
    def test_2_get_item_groups(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body, list)

    # Test to GET a single item group by ID
    def test_3_get_item_group_by_id(self):
        # Query parameter for ID
        response = self.client.get(f"{self.baseUrl}?id=101")
        self.assertIn(response.status_code, [200, 201])
        body = response.json()
        self.assertEqual(body[0].get("id"), self.TEST_BODY["id"])
        self.assertEqual(body[0].get("name"), self.TEST_BODY["name"])
        self.assertEqual(body[0].get("description"),
                         self.TEST_BODY["description"])

    # Test to PUT (update) an item group
    def test_4_put_item_group(self):
        response = self.client.put(f"{self.baseUrl}101", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = self.client.get(f"{self.baseUrl}?id=101")
        body = response.json()
        self.assertEqual(body[0].get("name"), "Updated")
        self.assertEqual(body[0].get("description"), "Updated")
        self.assertTrue(match_date(body[0].get("updated_at"), date.today()))

    # Test to DELETE an item group
    def test_5_delete_item_group(self):
        response = self.client.delete(f"{self.baseUrl}101")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = self.client.get(self.baseUrl)
        self.assertFalse(check_id_exists(response.json(), 100))

    # Test unauthorized access by removing the API key
    def test_6_no_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    # Test with an incorrect API key
    def test_7_wrong_key(self):
        self.client.headers = {"api-key": "invalid",
                               "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
