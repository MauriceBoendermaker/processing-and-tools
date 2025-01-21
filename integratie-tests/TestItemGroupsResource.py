import unittest
from httpx import Client
from datetime import datetime
from CargoHubV2.app.services.api_key_service import APIKeyService
from CargoHubV2.app.database import SessionLocal
from CargoHubV2.app.models.api_key_model import APIKey


class TestItemGroupsResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests. We create a real API key in the test DB
        so that `role_required` dependency sees a valid key with 'Manager' scope.
        """
        cls.db = SessionLocal()
        cls.api_key_service = APIKeyService(cls.db)

        # Create a key with scope='Manager' and 30-day expiration
        # so test calls that pass "a1b2c3d4e5" will be valid.
        cls.api_key_service.create_api_key(
            key="a1b2c3d4e55",
            access_scope="Manager",
            expires_in_days=30
        )

    @classmethod
    def tearDownClass(cls):
        """
        Runs once after all tests. Optional: clean up the API key or close DB.
        Here, we just close the session.
        """
        cls.db.close()

    def setUp(self):
        """
        Runs before each test. We make sure the client has the correct headers,
        including the valid API key from above.
        """
        self.baseUrl = "http://localhost:3000/api/v2/item_groups/"
        self.client = Client()
        self.client.headers = {
            "api-key": "a1b2c3d4e55",      # The raw key we just inserted into DB
            "content-type": "application/json"
        }

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

    def test_1_post_item_group(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        print("DEBUG - POST item_group response status:", response.status_code)
        print("DEBUG - POST item_group response body:", response.text)
        self.assertIn(response.status_code, [200, 201])

    def test_2_get_item_groups(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body, list)

    def test_3_get_item_group_by_id(self):
        response = self.client.get(f"{self.baseUrl}?id=101")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), self.TEST_BODY["id"])
        self.assertEqual(body.get("name"), self.TEST_BODY["name"])
        self.assertEqual(body.get("description"),
                         self.TEST_BODY["description"])

    def test_4_put_item_group(self):
        response = self.client.put(f"{self.baseUrl}101", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = self.client.get(f"{self.baseUrl}?id=101")
        body = response.json()
        self.assertEqual(body.get("name"), self.ToPut["name"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_5_delete_item_group(self):
        response = self.client.delete(f"{self.baseUrl}101")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = self.client.get(f"{self.baseUrl}?id=101")
        self.assertEqual(response.status_code, 404)

    def test_6_no_key(self):
        # Overwrite headers to remove the API key entirely
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        # Your dependency raises a 422 if there's no 'api-key' header
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_key(self):
        # Overwrite with an invalid API key
        self.client.headers = {
            "api-key": "invalid",
            "content-type": "application/json"
        }
        response = self.client.get(self.baseUrl)
        # Your dependency likely raises a 403 for invalid keys
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
