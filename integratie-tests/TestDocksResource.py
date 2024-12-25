import unittest
from httpx import Client

class TestDocksResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Runs once before all tests in this class.
        """
        cls.baseUrl = "http://localhost:3000/api/v2/docks/"
        cls.client = Client()
        cls.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

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
        cls.created_id = None  # We'll store the created dock's ID here

    def test_1_post_dock(self):
        """
        Test creating a new dock.
        """
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200])
        body = response.json()

        # Store dock ID for subsequent tests
        type(self).created_id = body.get("id")
        self.assertIsNotNone(type(self).created_id, "Dock 'id' should not be None after creation")

    def test_2_get_all_docks(self):
        """
        Test retrieving all docks (GET /).
        """
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)

    def test_3a_get_dock_by_code(self):
        """
        Test retrieving a single dock by its 'code' (GET /?code=<code>).
        """
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("description"), self.TEST_BODY["description"])

    def test_3b_get_dock_by_id(self):
        """
        Test retrieving a single dock by its auto-incremented 'id' (GET /<id>).
        """
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "Dock 'id' is not set from test_1_post_dock")

        response = self.client.get(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), dock_id)
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("status"), self.TEST_BODY["status"])

    def test_4_put_dock(self):
        """
        Test updating the dock by its ID.
        """
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "created_id should not be None. Did test_1_post_dock run first?")

        response = self.client.put(f"{self.baseUrl}{dock_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Fetch again (by code, for example) to verify changes
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), self.ToPut["status"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_5_delete_dock(self):
        """
        Test deleting the dock by its ID.
        """
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "created_id should not be None.")
        response = self.client.delete(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)

        # After deleting, retrieving by code should return 404
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 404)

    def test_6_no_key(self):
        """
        Test calling the endpoint with no API key in headers.
        """
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        # Assuming no key returns a 422 or 403/401, adjust as needed.
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_key(self):
        """
        Test calling the endpoint with an incorrect API key.
        """
        self.client.headers = {"api-key": "wrong_key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        # Assuming wrong key returns 403, adjust as needed.
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
