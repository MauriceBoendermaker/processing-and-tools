import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_code_exists

class TestDockResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/docks/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 1
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
            "warehouse_id": self.TEST_WAREHOUSE_ID,
            "code": self.TEST_CODE,
            "status": "inactive",
            "description": "Updated dock description",
            "is_deleted": True,
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
        }

    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["warehouse_id"], self.TEST_BODY["warehouse_id"])
        self.assertEqual(body["code"], self.TEST_BODY["code"])
        self.assertEqual(body["status"], self.TEST_BODY["status"])
        self.assertEqual(body["description"], self.TEST_BODY["description"])
        self.assertFalse(body["is_deleted"])

    def test_1_post_dock_integrity_error(self):
        # Creating the same dock again should result in a 400 error (duplicate)
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 400)
        self.assertIn("exists", response.json().get("detail"))

    def test_2_get_docks(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_code_exists(body, self.TEST_CODE))

    def test_3_get_dock_by_code(self):
        response = self.client.get(f"{self.baseUrl}?code={self.TEST_CODE}")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body["warehouse_id"], self.TEST_BODY["warehouse_id"])
        self.assertEqual(body["code"], self.TEST_CODE)
        self.assertEqual(body["status"], "active")
        self.assertEqual(body["description"], "Test dock description")

    def test_3_get_dock_notfound(self):
        response = self.client.get(f"{self.baseUrl}?code=non-existing-code")
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", body.get("detail"))

    def test_4_put_dock(self):
        response = self.client.put(f"{self.baseUrl}{self.TEST_CODE}", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?code={self.TEST_CODE}")
        body = response.json()
        self.assertEqual(body["status"], "inactive")
        self.assertEqual(body["description"], "Updated dock description")
        self.assertTrue(body["is_deleted"])
        self.assertTrue(match_date(body["updated_at"], date.today()))

    def test_4_put_dock_notfound(self):
        response = self.client.put(f"{self.baseUrl}non-existing-code", json=self.ToPut)
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", body.get("detail"))

    def test_5_delete_dock(self):
        # Teardown/cleanup
        response = self.client.delete(f"{self.baseUrl}{self.TEST_CODE}")

        self.assertEqual(response.status_code, 200)

        # Check if the dock is deleted
        na_delete = self.client.get(self.baseUrl)
        self.assertFalse(check_code_exists(na_delete.json(), self.TEST_CODE))

    def test_6_no_api_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 422)

    def test_7_wrong_api_key(self):
        self.client.headers = {"api-key": "randomguess", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()
