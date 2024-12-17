import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists

class TestDockResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://127.0.0.1:3000/api/v2/docks/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 99999
        self.TEST_BODY = {
            "id": self.TEST_ID,
            "warehouse_id": 101,
            "code": "D1",
            "status": "free",
            "description": "Dock 1 for loading",
        }

        self.ToPut = {
            "status": "occupied",
            "description": "Dock updated to occupied status."
        }

    # Test to create a dock using POST
    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [200, 201])
        body = response.json()
        self.assertEqual(body["code"], self.TEST_BODY["code"])
        self.assertEqual(body["status"], self.TEST_BODY["status"])

    # Test to get all docks using GET
    def test_2_get_docks(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(isinstance(body, list))
        self.assertTrue(len(body) > 0)

    # Test to get a single dock by ID using GET
    def test_3_get_dock_by_id(self):
        response = self.client.get(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["id"], self.TEST_ID)
        self.assertEqual(body["code"], self.TEST_BODY["code"])
        self.assertEqual(body["status"], self.TEST_BODY["status"])

    # Test to get docks by warehouse ID using GET
    def test_4_get_docks_by_warehouse(self):
        response = self.client.get(f"{self.baseUrl}warehouse/{self.TEST_BODY['warehouse_id']}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(isinstance(body, list))
        self.assertTrue(any(dock["warehouse_id"] == self.TEST_BODY["warehouse_id"] for dock in body))

    # Test to update a dock using PUT
    def test_5_put_dock(self):
        response = self.client.put(f"{self.baseUrl}{self.TEST_ID}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], self.ToPut["status"])
        self.assertEqual(body["description"], self.ToPut["description"])
        self.assertTrue(match_date(body["updated_at"], date.today()))

    # Test to delete a dock using DELETE
    def test_6_delete_dock(self):
        response = self.client.delete(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["detail"], "Dock deleted")

        # Verify it was deleted
        response = self.client.get(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 404)

    # Test unauthorized access by removing the API key
    def test_7_nokey(self):
        self.client.headers = {"content-type": "application/json"}  # Remove API key
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    # Test with an incorrect API key
    def test_8_wrong_key(self):
        self.client.headers = {"api-key": "invalid-key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()
