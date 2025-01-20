import unittest
from httpx import Client
from datetime import datetime
from CargoHubV2.app.main import app  # Replace with the actual FastAPI app import
from CargoHubV2.app.dependencies.api_dependencies import role_required, get_valid_api_key
from fastapi import Depends

# Mock dependencies for testing
def mock_valid_api_key(api_key: str):
    class MockAPIKey:
        access_scope = "Manager"

    return MockAPIKey()

def mock_role_required(allowed_roles):
    def mock_dependency(current_api_key=Depends(mock_valid_api_key)):
        return current_api_key

    return mock_dependency

# Apply dependency overrides
app.dependency_overrides[get_valid_api_key] = mock_valid_api_key
app.dependency_overrides[role_required] = mock_role_required

class TestClientResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/clients/"
        self.client = Client()
        self.client.headers = {
            "api-key": "a1b2c3d4e5",
            "content-type": "application/json"
        }

        self.TEST_BODY = {
            "id": 9838,
            "name": "test client",
            "address": "Carstenallee 2",
            "city": "Herzberg",
            "zip_code": "89685",
            "province": "Niedersachsen",
            "country": "Germany",
            "contact_name": "Ing. Ferdi Steckel MBA.",
            "contact_phone": "+49(0)5162 147719",
            "contact_email": "conradikati@example.net"
        }

        self.ToPut = {
            "address": "Wijnhaven 107",
            "city": "Rotterdam"
        }

    def test_1_post_client(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200])

    def test_2_get_clients(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body, list)

    def test_3_get_client(self):
        response = self.client.get(f"{self.baseUrl}?id=9838")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("id"), self.TEST_BODY["id"])
        self.assertEqual(body.get("name"), self.TEST_BODY["name"])
        self.assertEqual(body.get("address"), self.TEST_BODY["address"])
        self.assertEqual(body.get("city"), self.TEST_BODY["city"])

    def test_4_put_client(self):
        response = self.client.put(f"{self.baseUrl}9838", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?id=9838")
        body = response.json()
        self.assertEqual(body.get("address"), self.ToPut["address"])
        self.assertEqual(body.get("city"), self.ToPut["city"])

    def test_5_delete_client(self):
        response = self.client.delete(f"{self.baseUrl}9838")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?id=9838")
        self.assertEqual(response.status_code, 404)

    def test_6_no_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_key(self):
        self.client.headers = {
            "api-key": "invalid-key",
            "content-type": "application/json"
        }
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)

if __name__ == "__main__":
    unittest.main()
