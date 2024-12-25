import unittest
from httpx import Client

class TestDocksResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseUrl = "http://localhost:3000/api/v2/docks/"
        cls.client = Client()
        cls.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        # Data for creating a new dock
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

        cls.created_id = None  # We'll store the dock's auto-increment ID after creation

    def test_1_post_dock(self):
        # Create a dock, ensure 201 or 200
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200])
        body = response.json()

        # Store the dock's auto-incremented ID in the class
        type(self).created_id = body.get("id")
        self.assertIsNotNone(type(self).created_id, "Dock 'id' should not be None after creation.")

    def test_2_get_all_docks(self):
        # Retrieve all docks, expect 200
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)

    def test_3_get_dock_by_code(self):
        # Retrieve a single dock by code
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("description"), self.TEST_BODY["description"])

    def test_4_get_dock_by_id(self):
        # Retrieve the same dock by ID
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "Dock ID is not set from test_1_post_dock")

        response = self.client.get(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), dock_id)
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])

    def test_5_put_dock(self):
        # Update the dock by ID
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id)

        response = self.client.put(f"{self.baseUrl}{dock_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Verify changes via code or ID
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), self.ToPut["status"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_6_delete_dock(self):
        # Delete the dock by ID
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id)

        response = self.client.delete(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)

        # Verify it's gone by code
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 404)

    def test_7_no_key(self):
        # Test calling with no API key
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    def test_8_wrong_key(self):
        # Test calling with the wrong API key
        self.client.headers = {"api-key": "wrong_key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
