import unittest
from fastapi.testclient import TestClient, Depends
from datetime import date
from CargoHubV2.app.main import app  # Replace with the actual FastAPI app import
from CargoHubV2.app.dependencies.api_dependencies import role_required, get_valid_api_key

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


class TestItemsResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/items/"
        self.client = TestClient(app)
        self.client.headers = {"api-key": "mocked-key",
                               "content-type": "application/json"}

        self.TEST_BODY = {
            "uid": "P011724",
            "code": "tijdelijke-item69",
            "description": "Face-to-face clear-thinking complexity",
            "short_description": "must",
            "upc_code": "6523540947122",
            "model_number": "63-OFFTq0T",
            "commodity_code": "oTo304",
            "item_line": 11,
            "item_group": 73,
            "item_type": 14,
            "unit_purchase_quantity": 47,
            "unit_order_quantity": 13,
            "pack_order_quantity": 11,
            "supplier_id": 34,
            "supplier_code": "SUP423",
            "supplier_part_number": "E-86805-uTM",
            "created_at": "2015-02-19 16:08:24",
            "updated_at": "2015-09-26 06:37:56",
            "hazard_classification": "Compressed gas"
        }

        self.ToPut = {
            "description": "Updated complexity description",
            "short_description": "updated"
        }

    def test_1_post_item(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertIn(response.status_code, [201, 200])

    def test_2_get_items(self):
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIsInstance(body, list)

    def test_3_get_item(self):
        response = self.client.get(f"{self.baseUrl}?code=tijdelijke-item69")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("code"), self.TEST_BODY["code"])
        self.assertEqual(body.get("description"),
                         self.TEST_BODY["description"])
        self.assertEqual(body.get("item_group"), self.TEST_BODY["item_group"])

    def test_4_put_item(self):
        response = self.client.put(
            f"{self.baseUrl}tijdelijke-item69", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?code=tijdelijke-item69")
        body = response.json()
        self.assertEqual(body.get("short_description"),
                         self.ToPut["short_description"])
        self.assertEqual(body.get("description"), self.ToPut["description"])

    def test_5_delete_item(self):
        response = self.client.delete(f"{self.baseUrl}tijdelijke-item69")
        self.assertEqual(response.status_code, 200)

        item_data = response.json()
        self.assertIn("is_deleted", item_data)
        self.assertTrue(item_data["is_deleted"])

    def test_6_no_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    def test_7_wrong_key(self):
        self.client.headers = {"api-key": "invalid-key",
                               "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
