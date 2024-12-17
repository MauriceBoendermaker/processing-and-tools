import unittest
from httpx import Client
from datetime import datetime
from test_utils import check_id_exists, match_date

class TestDocksResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/docks/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 999
        self.TEST_BODY = {
            "warehouse_id": 1,
            "code": "DOCK_TEST_1",
            "status": "free",
            "description": "Test Dock for Warehouse 1"
        }

        self.ToPut = {"status": "occupied", "description": "Updated test dock"}

    # 1. Test POST - Create a dock
    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["code"], self.TEST_BODY["code"])
        self.assertEqual(body["status"], self.TEST_BODY["status"])

    # 2. Test GET all docks with sorting
    def test_2_get_all_docks(self):
        response = self.client.get(f"{self.baseUrl}?sort_by=code&order=asc")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(any(dock["code"] == self.TEST_BODY["code"] for dock in body))

    # 3. Test GET dock by ID
    def test_3_get_dock_by_id(self):
        response = self.client.get(f"{self.baseUrl}1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["code"], "DOCK_TEST_1")

    # 4. Test PUT - Update dock
    def test_4_update_dock(self):
        response = self.client.put(f"{self.baseUrl}1", json=self.ToPut)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], self.ToPut["status"])
        self.assertTrue(match_date(body["updated_at"], datetime.today().date()))

    # 5. Test DELETE - Soft delete a dock
    def test_5_delete_dock(self):
        response = self.client.delete(f"{self.baseUrl}1")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["detail"], "Dock deleted")

        # Ensure it's soft deleted
        response = self.client.get(f"{self.baseUrl}1")
        self.assertEqual(response.status_code, 404)

    # 6. Test GET docks by warehouse ID
    def test_6_get_docks_by_warehouse(self):
        response = self.client.get(f"{self.baseUrl}warehouse/1?sort_by=code&order=asc")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(len(body) > 0)
        self.assertEqual(body[0]["warehouse_id"], 1)

    # 7. Test Unauthorized access
    def test_7_no_api_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    # 8. Test Wrong API key
    def test_8_wrong_api_key(self):
        self.client.headers = {"api-key": "invalid-key", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()
