import unittest
from httpx import Client


class TestDocksResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/docks/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}
        self.TEST_BODY = {
            "warehouse_id": 1,
            "code": "DCK001",
            "status": "Free",
            "description": "Test Dock"
        }
        self.ToPut = {
            "status": "Occupied",
            "description": "Updated Test Dock"
        }
        self.created_id = None  # Initialize to None

    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200])
        # Store the created_id at class level
        type(self).created_id = response.json().get("id")
        self.assertIsNotNone(type(self).created_id)

    def test_2_get_docks(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)

    def test_3_get_dock(self):
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("description"), self.TEST_BODY["description"])

    def test_4_put_dock(self):
        dock_id = type(self).created_id
        self.assertIsNotNone(dock_id, "created_id should not be None. Did test_1_post_dock run first?")
        response = self.client.put(f"{self.baseUrl}{dock_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Fetch again by code to verify changes
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

        # After deleting, getting by code should return 404
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        self.assertEqual(response.status_code, 404)

    def test_6_no_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        # Assuming no key returns a 422 or some error code
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_key(self):
        self.client.headers = {"api-key": "wrong_key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        # Assuming wrong key returns 403
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
