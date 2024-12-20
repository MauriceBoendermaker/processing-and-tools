import unittest
from httpx import Client
from datetime import datetime
from test_utils import check_code_exists


class TestDocksResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/docks/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_BODY = {
            "warehouse_id": 1,
            "code": "DCK001",
            "status": "free",
            "description": "Test Dock",
            "created_at": "2024-12-20 12:00:00",  # DateTime format
            "updated_at": "2024-12-20 12:00:00",  # DateTime format
            "is_deleted": False
        }

        self.ToPut = {
            "status": "occupied",
            "description": "Updated Test Dock",
            "updated_at": "2024-12-21 12:00:00",  # Updated DateTime
        }

    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200])

    def test_2_get_docks(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        # self.assertTrue(check_code_exists(body, "DCK001"))

    def test_3_get_dock(self):
        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("description"), self.TEST_BODY["description"])
        self.assertEqual(body.get("status"), self.TEST_BODY["status"])

    def test_4_put_dock(self):
        response = self.client.put(f"{self.baseUrl}DCK001", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?code=DCK001")
        body = response.json()
        self.assertEqual(body.get("status"), self.ToPut["status"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_5_delete_dock(self):
        response = self.client.delete(f"{self.baseUrl}DCK001")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(self.baseUrl)
        self.assertFalse(check_code_exists(response.json(), "DCK001"))

    def test_6_no_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_key(self):
        self.client.headers = {"api-key": "wrong_key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
