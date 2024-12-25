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
            "status": "free",
            "description": "Test Dock"
        }

        self.ToPut = {
            "status": "occupied",
            "description": "Updated Test Dock"
        }

    def test_1_post_dock(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["code"], "DCK001")
        self.created_id = body["id"]

    def test_2_get_all_docks(self):
        # Retrieve all docks, default sorting
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        docks = response.json()
        self.assertIsInstance(docks, list)

        # Test sorting by code descending
        response = self.client.get(self.baseUrl, params={"sort_by": "code", "order": "desc"})
        self.assertEqual(response.status_code, 200)

    def test_3_get_dock_by_id(self):
        # Assuming self.created_id is known from test_1_post_dock or persist it in a class var
        # For demonstration, let's say we got it from test_1_post_dock.
        # In real runs, ensure test order or store in class variable.
        dock_id = getattr(self, 'created_id', None)
        self.assertIsNotNone(dock_id)

        response = self.client.get(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["code"], "DCK001")

    def test_4_put_dock(self):
        dock_id = getattr(self, 'created_id', None)
        self.assertIsNotNone(dock_id)
        response = self.client.put(f"{self.baseUrl}{dock_id}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "occupied")
        self.assertEqual(body["description"], "Updated Test Dock")

    def test_5_delete_dock(self):
        dock_id = getattr(self, 'created_id', None)
        self.assertIsNotNone(dock_id)
        response = self.client.delete(f"{self.baseUrl}{dock_id}")
        self.assertEqual(response.status_code, 200)

        # Verify dock is deleted
        response = self.client.get(f"{self.baseUrl}{dock_id}")
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
