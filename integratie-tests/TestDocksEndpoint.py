import unittest
from httpx import Client
from datetime import datetime
from test_utils import check_code_exists, check_id_exists, match_date  # Assuming you have utility functions for validation

class TestDockResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/docks/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 99999  # The test ID (this can be auto-generated, but fixed for consistency)
        self.TEST_CODE = "DOCKTEST"

        self.TEST_BODY = {
            "warehouse_id": 1,
            "code": self.TEST_CODE,
            "status": "active",
            "created_at": "2024-12-19T10:00:00",
            "updated_at": "2024-12-19T10:00:00",
        }

        self.ToPut = {
            "status": "inactive",
            "updated_at": "2024-12-19T10:30:00",
        }

        # Added dock_data as a common test resource
        self.dock_data = self.TEST_BODY

    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("code"), self.TEST_BODY["code"])
        self.assertEqual(response.json().get("status"), self.TEST_BODY["status"])
        
        # Ensure a valid dock ID is returned
        dock_id = response.json().get("id")
        self.assertIsNotNone(dock_id, "Dock ID should not be None")
        self.dock_id = dock_id  # Store the created dock's ID for reuse in other tests

    def test_1_post_dock_integrity_error(self):
        # Trying to create a dock with the same code should raise an integrity error.
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 400)
        self.assertIn("exists", response.json().get("detail"))

    def test_2_get_all_docks(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_code_exists(body, self.TEST_CODE))

    def test_3_get_dock_by_id(self):
        # Ensure dock exists before querying.
        if not hasattr(self, 'dock_id'):  # If the dock hasn't been created yet, create it
            response = self.client.post(self.baseUrl, json=self.dock_data)
            self.dock_id = response.json().get("id")

        # Query the dock by ID.
        response = self.client.get(f"{self.baseUrl}{self.dock_id}")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), self.dock_id)

    def test_3_get_dock_not_found(self):
        response = self.client.get(f"{self.baseUrl}999999")  # Assuming this ID doesn't exist
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("Dock not found", body.get("detail"))

    def test_4_put_dock(self):
        # Ensure dock exists before updating.
        if not hasattr(self, 'dock_id'):  # If the dock hasn't been created yet, create it
            response = self.client.post(self.baseUrl, json=self.dock_data)
            self.dock_id = response.json().get("id")

        # Define the updated data.
        updated_data = {
            "status": "inactive",
            "updated_at": "2024-12-19T10:30:00",
        }

        # Send the PUT request to update the dock.
        response = self.client.put(f"{self.baseUrl}{self.dock_id}", json=updated_data)
        
        self.assertEqual(response.status_code, 200)
        updated_dock = self.client.get(f"{self.baseUrl}{self.dock_id}").json()
        self.assertEqual(updated_dock["status"], "inactive")

    def test_4_put_dock_not_found(self):
        response = self.client.put(f"{self.baseUrl}999999", json=self.ToPut)
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("Dock not found", body.get("detail"))

    def test_5_delete_dock(self):
        # Ensure dock exists before deleting.
        if not hasattr(self, 'dock_id'):  # If the dock hasn't been created yet, create it
            response = self.client.post(self.baseUrl, json=self.dock_data)
            self.dock_id = response.json().get("id")

        # Delete the dock.
        response = self.client.delete(f"{self.baseUrl}{self.dock_id}")
        
        self.assertEqual(response.status_code, 200)

        # Verify dock is deleted by trying to retrieve it.
        response = self.client.get(f"{self.baseUrl}{self.dock_id}")
        self.assertEqual(response.status_code, 404)  # Expect 404 after deletion

    def test_5_delete_dock_not_found(self):
        # Trying to delete a non-existent dock
        response = self.client.delete(f"{self.baseUrl}999999")
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("Dock not found", body.get("detail"))

    def test_6_no_api_key(self):
        self.client.headers = {"content-type": "application/json"}  # Removing the API key
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_api_key(self):
        self.client.headers = {"api-key": "wrongapikey", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
