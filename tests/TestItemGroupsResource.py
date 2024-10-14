import unittest
from httpx import Client


class TestItemGroupsResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/item_groups"
        self.client = Client()
        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}

        self.expected_body = {
            "id": 1,
            "name": "Furniture",
            "description": "",
            "created_at": "2019-09-22 15:51:07",
            "updated_at": "2022-05-18 13:49:28"
        }

    # Test 1: Get data for an existing item_group (valid data)
    def test_1_get_item_group(self):
        response = self.client.get(f"{self.baseUrl}/1")
        body = response.json()

        self.assertEqual(response.status_code, 200)  # Status should be OK
        self.assertEqual(body.get("id"), self.expected_body["id"])
        self.assertEqual(body.get("name"), self.expected_body["name"])
        self.assertEqual(body.get("description"),
                         self.expected_body["description"])

    def test_2_get_non_existing_item_group(self):
        response = self.client.get(f"{self.baseUrl}/99999")  # Non-existing ID
        body = response.json()

        # Check if the body is empty or it returned none
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body, None)

    # Test 3: Unauthorized access (missing API key)

    def test_3_get_item_group_unauthorized(self):
        # Remove API key to simulate unauthorized access
        self.client.headers = {
            "content-type": "application/json"}  # No API_KEY
        response = self.client.get(f"{self.baseUrl}/0")
        # Expecting 401 Unauthorized
        self.assertEqual(response.status_code, 401)

    def test_4_get_item_group_invalid_id(self):
        response = self.client.get(f"{self.baseUrl}/invalid_id")  # Using a string instead of an int
        self.assertEqual(response.status_code, 500)  # Expecting a 500 server error

    def test_5_get_item_group_server_error(self):
        response = self.client.get(f"{self.baseUrl}/999999999999999999999999")  # Using an extremely large ID
        self.assertEqual(response.status_code, 200)  # Expecting a 200 because api doesnt check if id exists correctly




if __name__ == '__main__':
    unittest.main()
