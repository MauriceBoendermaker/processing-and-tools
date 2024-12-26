import unittest
from httpx import Client
from datetime import datetime
from test_utils import check_code_exists  # Ensure this utility is updated if needed


class TestDocksEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Initialize the test client and set up test data.
        This runs once before all tests.
        """
        cls.baseUrl = "http://localhost:3000/api/v2/docks/"
        cls.client = Client()
        cls.api_key = "a1b2c3d4e5"
        cls.client.headers.update({
            "api-key": cls.api_key,
            "content-type": "application/json"
        })

        cls.TEST_BODY = {
            "warehouse_id": 1,
            "code": "DCK001",
            "status": "free",
            "description": "Test Dock"
        }

        cls.ToPut = {
            "status": "occupied",
            "description": "Updated Test Dock"
        }

        cls.created_id = None  # Will store the ID of the created dock

    @classmethod
    def tearDownClass(cls):
        """
        Clean up any remaining test data after all tests have run.
        """
        if cls.created_id:
            response = cls.client.delete(f"{cls.baseUrl}{cls.created_id}")
            # Optionally, check if deletion was successful
            if response.status_code not in [200, 404]:
                print(f"Failed to delete dock with ID {cls.created_id} during teardown.")

    def test_1_post_dock(self):
        """
        Test creating a new dock.
        """
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200], msg="Failed to create dock.")

        response_data = response.json()
        self.assertIsNotNone(response_data.get("id"), msg="Created dock does not have an 'id'.")
        self.assertEqual(response_data["code"], self.TEST_BODY["code"], msg="Dock code mismatch.")
        self.assertEqual(response_data["status"], self.TEST_BODY["status"], msg="Dock status mismatch.")
        self.assertEqual(response_data["description"], self.TEST_BODY["description"], msg="Dock description mismatch.")
        self.assertFalse(response_data["is_deleted"], msg="New dock should not be deleted.")

        # Store the created_id for use in subsequent tests
        self.__class__.created_id = response_data["id"]

    def test_2_get_docks_with_sorting(self):
        """
        Test retrieving all docks with sorting parameters.
        """
        # Ensure that sort_by and order are provided
        params = {
            "sort_by": "id",
            "order": "asc"
        }
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 200, msg="Failed to retrieve docks with sorting.")

        docks = response.json()
        self.assertIsInstance(docks, list, msg="Docks response should be a list.")
        self.assertGreaterEqual(len(docks), 1, msg="There should be at least one dock.")

        # Optionally, verify that the docks are sorted by 'id' in ascending order
        ids = [dock["id"] for dock in docks]
        self.assertEqual(ids, sorted(ids), msg="Docks are not sorted by 'id' in ascending order.")

    def test_3_get_dock_by_id(self):
        """
        Test retrieving a single dock by its 'id'.
        """
        dock_id = self.__class__.created_id
        self.assertIsNotNone(dock_id, msg="created_id is not set. 'test_1_post_dock' might have failed.")

        params = {"id": dock_id, "sort_by": "id", "order": "asc"}  # Include required sorting params
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 200, msg="Failed to retrieve dock by 'id'.")

        dock = response.json()
        self.assertEqual(dock.get("id"), dock_id, msg="Retrieved dock ID does not match.")
        self.assertEqual(dock.get("code"), self.TEST_BODY["code"], msg="Dock code mismatch.")
        self.assertEqual(dock.get("description"), self.TEST_BODY["description"], msg="Dock description mismatch.")
        self.assertEqual(dock.get("status"), self.TEST_BODY["status"], msg="Dock status mismatch.")
        self.assertFalse(dock.get("is_deleted"), msg="Dock should not be deleted.")

    def test_4_put_dock(self):
        """
        Test updating an existing dock.
        """
        dock_id = self.__class__.created_id
        self.assertIsNotNone(dock_id, msg="created_id is not set. 'test_1_post_dock' might have failed.")

        response = self.client.put(f"{self.baseUrl}{dock_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 200, msg="Failed to update dock.")

        updated_dock = response.json()
        self.assertEqual(updated_dock.get("status"), self.ToPut["status"], msg="Dock status was not updated.")
        self.assertEqual(updated_dock.get("description"), self.ToPut["description"], msg="Dock description was not updated.")

        # Verify the updates via a GET request
        params = {"id": dock_id, "sort_by": "id", "order": "asc"}
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 200, msg="Failed to retrieve updated dock.")

        dock = response.json()
        self.assertEqual(dock.get("status"), self.ToPut["status"], msg="Dock status mismatch after update.")
        self.assertEqual(dock.get("description"), self.ToPut["description"], msg="Dock description mismatch after update.")

    def test_5_delete_dock(self):
        """
        Test soft deleting a dock.
        """
        dock_id = self.__class__.created_id
        self.assertIsNotNone(dock_id, msg="created_id is not set. 'test_1_post_dock' might have failed.")

        response = self.client.delete(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200, msg="Failed to delete dock.")

        # Verify that the dock is soft-deleted
        params = {"id": dock_id, "sort_by": "id", "order": "asc"}
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 404, msg="Deleted dock should not be retrievable.")

    def test_6_no_api_key(self):
        """
        Test accessing the endpoint without providing an API key.
        """
        original_headers = self.client.headers.copy()
        self.client.headers = {"content-type": "application/json"}  # Remove api-key

        params = {"sort_by": "id", "order": "asc"}
        response = self.client.get(self.baseUrl, params=params)
        self.assertIn(response.status_code, [401, 422], msg="Access without API key should be unauthorized or invalid.")

        self.client.headers = original_headers  # Restore original headers

    def test_7_wrong_api_key(self):
        """
        Test accessing the endpoint with an invalid API key.
        """
        original_headers = self.client.headers.copy()
        self.client.headers = {"api-key": "wrong_key", "content-type": "application/json"}

        params = {"sort_by": "id", "order": "asc"}
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 403, msg="Access with wrong API key should be forbidden.")

        self.client.headers = original_headers  # Restore original headers

    def test_8_missing_sort_by(self):
        """
        Test retrieving docks without providing 'sort_by' parameter.
        """
        params = {"order": "asc"}  # Missing sort_by
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 400, msg="Missing 'sort_by' should return 400 Bad Request.")
        self.assertIn("sort_by parameter is required", response.text, msg="Error message for missing 'sort_by' not found.")

    def test_9_missing_order(self):
        """
        Test retrieving docks without providing 'order' parameter.
        """
        params = {"sort_by": "id"}  # Missing order
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 400, msg="Missing 'order' should return 400 Bad Request.")
        self.assertIn("order parameter is required", response.text, msg="Error message for missing 'order' not found.")

    def test_10_invalid_sort_by(self):
        """
        Test retrieving docks with an invalid 'sort_by' parameter.
        """
        params = {"sort_by": "invalid_field", "order": "asc"}
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 400, msg="Invalid 'sort_by' should return 400 Bad Request.")
        self.assertIn("Invalid sort field", response.text, msg="Error message for invalid 'sort_by' not found.")

    def test_11_invalid_order(self):
        """
        Test retrieving docks with an invalid 'order' parameter.
        """
        params = {"sort_by": "id", "order": "invalid_order"}
        response = self.client.get(self.baseUrl, params=params)
        self.assertEqual(response.status_code, 400, msg="Invalid 'order' should return 400 Bad Request.")
        self.assertIn("Invalid order parameter", response.text, msg="Error message for invalid 'order' not found.")

    def test_12_create_duplicate_code(self):
        """
        Test creating a dock with a duplicate 'code'.
        """
        # First, create a dock with a unique code
        unique_code = "DCK_UNIQUE"
        test_body = {
            "warehouse_id": 2,
            "code": unique_code,
            "status": "free",
            "description": "Unique Test Dock"
        }
        response = self.client.post(self.baseUrl, json=test_body)
        self.assertIn(response.status_code, [201, 200], msg="Failed to create dock with unique code.")

        # Attempt to create another dock with the same code
        response = self.client.post(self.baseUrl, json=test_body)
        self.assertEqual(response.status_code, 400, msg="Creating dock with duplicate 'code' should fail.")
        self.assertIn("A dock with this code already exists", response.text, msg="Expected error message for duplicate 'code' not found.")

        # Clean up by deleting the created dock
        if response.status_code in [201, 200]:
            created_id = response.json().get("id")
            if created_id:
                self.client.delete(f"{self.baseUrl}{created_id}")

    def test_13_create_dock_missing_fields(self):
        """
        Test creating a dock with missing required fields.
        """
        incomplete_body = {
            "code": "DCK_MISSING_WAREHOUSE",
            "status": "free"
            # Missing 'warehouse_id'
        }
        response = self.client.post(self.baseUrl, json=incomplete_body)
        self.assertIn(response.status_code, [400, 422], msg="Creating dock with missing fields should fail.")
        self.assertIn("warehouse_id", response.text, msg="Error message for missing 'warehouse_id' not found.")

    def test_14_update_nonexistent_dock(self):
        """
        Test updating a dock that does not exist.
        """
        nonexistent_id = 999999  # Assuming this ID does not exist
        response = self.client.put(f"{self.baseUrl}{nonexistent_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 404, msg="Updating nonexistent dock should return 404 Not Found.")
        self.assertIn("Dock not found", response.text, msg="Error message for nonexistent dock not found.")

    def test_15_delete_nonexistent_dock(self):
        """
        Test deleting a dock that does not exist.
        """
        nonexistent_id = 999999  # Assuming this ID does not exist
        response = self.client.delete(f"{self.baseUrl}{nonexistent_id}")
        self.assertEqual(response.status_code, 404, msg="Deleting nonexistent dock should return 404 Not Found.")
        self.assertIn("Dock not found", response.text, msg="Error message for nonexistent dock not found.")


if __name__ == '__main__':
    unittest.main()
