import unittest
from httpx import Client

class TestDocksResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This runs once before all tests.
        We configure the client, baseUrl, and test data here.
        """
        cls.baseUrl = "http://localhost:3000/api/v2/docks/"
        cls.client = Client()
        # Mock API key and headers
        cls.client.headers = {
            "api-key": "a1b2c3d4e5",
            "content-type": "application/json"
        }

        # Sample data for creating a new dock
        cls.TEST_BODY = {
            "warehouse_id": 1,
            "code": "DCK001",
            "status": "free",
            "description": "Integration Test Dock"
        }

        # Data for updating the dock
        cls.ToPut = {
            "status": "occupied",
            "description": "Updated Integration Test Dock"
        }

        # We'll store the dock ID once we create it
        cls.created_id = None

    def test_1_post_dock(self):
        """
        Test creating a new dock.
        We expect a 201 status code (or 200 if your endpoint still returns 200).
        We'll store the resulting dock's ID for the next tests.
        """
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200], 
                      msg=f"Expected 201 or 200, got {response.status_code}")

        body = response.json()
        # Store the dock ID in the class so other tests can use it
        type(self).created_id = body.get("id")
        self.assertIsNotNone(type(self).created_id, "Dock 'id' should not be None after creation")

    def test_2_get_all_docks(self):
        """
        Test retrieving all docks.
        We expect status code 200 and a list in the response.
        """
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected 200, got {response.status_code}")
        self.assertIsInstance(response.json(), list, "GET /api/v2/docks should return a list")

    def test_3_get_dock_by_id(self):
        """
        Test retrieving the specific dock by its auto-incremented ID.
        We expect 200 and the correct dock data.
        """
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "Dock ID is not set from test_1_post_dock")

        response = self.client.get(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected 200 when fetching dock {dock_id}, got {response.status_code}")

        body = response.json()
        self.assertEqual(body.get("id"), dock_id)
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("description"), self.TEST_BODY["description"])

    def test_4_put_dock(self):
        """
        Test updating the dock by its ID.
        We expect 200 and see that the fields have changed.
        """
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "Dock ID is not set from test_1_post_dock")

        response = self.client.put(f"{self.baseUrl}{dock_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected 200 when updating dock {dock_id}, got {response.status_code}")

        # Fetch the dock again by ID to verify the changes
        response = self.client.get(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), self.ToPut["status"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_5_delete_dock(self):
        """
        Test deleting the dock by its ID.
        We expect 200, then a subsequent fetch by ID should return 404.
        """
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "Dock ID is not set from test_1_post_dock")

        response = self.client.delete(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200,
                         msg=f"Expected 200 when deleting dock {dock_id}, got {response.status_code}")

        # Attempt to retrieve the deleted dock -> expect 404
        response = self.client.get(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 404,
                         msg=f"Expected 404 after deleting dock {dock_id}, got {response.status_code}")


if __name__ == '__main__':
    unittest.main()