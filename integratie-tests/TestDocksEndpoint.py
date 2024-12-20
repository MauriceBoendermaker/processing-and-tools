import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_code_exists

class TestDockResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/docks/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_WAREHOUSE_ID = 1
        self.TEST_CODE = "TESTDOCK"

        self.TEST_BODY = {
            "warehouse_id": self.TEST_WAREHOUSE_ID,
            "code": self.TEST_CODE,
            "status": "active",
            "description": "Test dock description",
            "is_deleted": False,
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
        }

        self.ToPut = {
            "status": "inactive",
            "description": "Updated dock description"
        }

    def test_1_post_dock(self):
        """
        Test creating a new dock.
        """
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["code"], self.TEST_CODE)
        self.assertEqual(body["status"], self.TEST_BODY["status"])
        self.assertEqual(body["description"], self.TEST_BODY["description"])

    def test_1_post_dock_integrity_error(self):
        """
        Test creating a dock with duplicate code (should return error 400).
        """
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 400)
        self.assertIn("exists", response.json().get("detail"))

    def test_2_get_docks(self):
        """
        Test retrieving all docks.
        """
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(isinstance(body, list))
        self.assertTrue(check_code_exists(body, self.TEST_CODE))

    def test_3_get_dock_by_code(self):
        """
        Test retrieving a dock by its code.
        """
        response = self.client.get(f"{self.baseUrl}?code={self.TEST_CODE}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["code"], self.TEST_CODE)
        self.assertEqual(body["status"], "active")
        self.assertEqual(body["description"], "Test dock description")

    def test_3_get_dock_notfound(self):
        """
        Test retrieving a non-existing dock (should return 404).
        """
        response = self.client.get(f"{self.baseUrl}?code=NONEXISTENT")
        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertIn("not found", body["detail"])

    def test_4_put_dock(self):
        """
        Test updating an existing dock.
        """
        response = self.client.put(f"{self.baseUrl}{self.TEST_CODE}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Verify updates
        response = self.client.get(f"{self.baseUrl}?code={self.TEST_CODE}")
        body = response.json()
        self.assertEqual(body["status"], "inactive")
        self.assertEqual(body["description"], "Updated dock description")
        self.assertTrue(match_date(body["updated_at"], date.today()))

    def test_4_put_dock_notfound(self):
        """
        Test updating a non-existing dock (should return 404).
        """
        response = self.client.put(f"{self.baseUrl}NONEXISTENT", json=self.ToPut)
        self.assertEqual(response.status_code, 404)
        body = response.json()
        self.assertIn("not found", body["detail"])

    def test_5_delete_dock(self):
        """
        Test deleting a dock.
        """
        response = self.client.delete(f"{self.baseUrl}{self.TEST_CODE}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = self.client.get(f"{self.baseUrl}?code={self.TEST_CODE}")
        self.assertEqual(response.status_code, 404)

    def test_6_no_api_key(self):
        """
        Test request without an API key (should return 422).
        """
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_api_key(self):
        """
        Test request with an incorrect API key (should return 403).
        """
        self.client.headers = {"api-key": "wrongkey", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()
