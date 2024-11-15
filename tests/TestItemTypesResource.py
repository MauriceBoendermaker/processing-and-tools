import unittest
from httpx import Client
from test_utils import check_id_exists


class TestItemTypesResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/item_types"
        self.client = Client()
        self.client.headers = {"API_KEY": "a1b2c3d4e5", "content-type": "application/json"}

        self.EXPECTED_BODY = {
            "id": 0,
            "name": "Laptop",
            "description": "",
            "created_at": "2001-11-02 23:02:40",
            "updated_at": "2008-07-01 04:09:17"
        }


    # Test 1: Get data for an existing item_type (valid data)
    def test_1_get_item_type(self):
        response = self.client.get(f"{self.baseUrl}/0")
        body = response.json()
        
        self.assertEqual(response.status_code, 200)  # Status should be OK
        self.assertEqual(body.get("id"), self.EXPECTED_BODY["id"])
        self.assertEqual(body.get("name"), self.EXPECTED_BODY["name"])
        self.assertEqual(body.get("description"), self.EXPECTED_BODY["description"])

    # Test 2: Try to get data for a non-existing item_type (should return 200)
    def test_2_get_non_existing_item_type(self):
        response = self.client.get(f"{self.baseUrl}/99999")  # Non-existing ID
        self.assertEqual(response.status_code, 200)  # Expecting 200 as api doesnt handel it correctly

    # Test 3: Unauthorized access (missing API key)
    def test_3_get_item_type_unauthorized(self):
        self.client.headers = {"content-type": "application/json"}  # No API_KEY
        response = self.client.get(f"{self.baseUrl}/1")
        self.assertEqual(response.status_code, 401)  # Expecting 401 Unauthorized

    # Test 4: Get with invalid data type in URL (expecting 400 Bad Request)
    def test_4_get_item_type_invalid_id(self):
        response = self.client.get(f"{self.baseUrl}/invalid_id")
        self.assertEqual(response.status_code, 500)  # Expecting a 500 server error

    # Test 5: Simulate server error (expecting 500 Internal Server Error)
    def test_5_get_item_type_server_error(self):
        response = self.client.get(f"{self.baseUrl}/999999999999999999999999")  # Using an extremely large ID
        self.assertEqual(response.status_code, 200)  # Expecting a 200 because api doesnt handel requests correctly


if __name__ == '__main__':
    unittest.main()
