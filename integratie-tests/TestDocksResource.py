import unittest
from httpx import Client

class TestDocksResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
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
        cls.created_id = None

        # Create dock for testing
        response = cls.client.post(cls.baseUrl, json=cls.TEST_BODY)
        if response.status_code in [200, 201]:
            cls.created_id = response.json().get("id")
        else:
            raise Exception("Failed to create test dock for integration tests.")

    @classmethod
    def tearDownClass(cls):
        # Cleanup dock after tests
        if cls.created_id:
            cls.client.delete(f"{cls.baseUrl}{cls.created_id}")

    def tearDown(self):
        # Reset headers after tests that modify them
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200])
        dock_id = response.json().get("id")
        self.assertIsNotNone(dock_id)

    def test_2_get_docks(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body, list)
        if body:
            self.assertIn("id", body[0])
            self.assertIn("warehouse_id", body[0])

    def test_3_get_dock(self):
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("description"), self.TEST_BODY["description"])

    def test_4_put_dock(self):
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "created_id should not be None.")
        response = self.client.put(f"{self.baseUrl}{dock_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Verify changes
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), self.ToPut["status"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_5_delete_dock(self):
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "created_id should not be None.")
        response = self.client.delete(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 404)

    def test_6_no_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)  # Update based on API behavior

    def test_7_wrong_key(self):
        self.client.headers = {"api-key": "wrong_key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)

    def test_8_pagination(self):
        response = self.client.get(f"{self.baseUrl}?offset=0&limit=1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body, list)
        self.assertLessEqual(len(body), 1)

if __name__ == "__main__":
    unittest.main()
