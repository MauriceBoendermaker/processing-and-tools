import unittest
from httpx import Client
from test_utils import match_date, check_id_exists
from datetime import date

class TestTransfersResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/transfers"
        self.client = Client()

        self.test_body = {
            "id": 119241,
            "reference": "TR119241",
            "transfer_from": None,
            "transfer_to": 9200,
            "transfer_status": "Scheduled",
            "created_at": "2024-10-14T12:00:00Z",
            "updated_at": "2024-10-14T12:00:00Z",
            "items": [
                {
                    "item_id": "P001288",
                    "amount": 15
                }
            ]
        }

        self.ToPut = {
            "id": 119241,
            "reference": "TR119241",
            "transfer_from": 9200,
            "transfer_to": 9201,
            "transfer_status": "In Progress",
            "created_at": "2024-10-14T12:00:00Z",
            "updated_at": "2024-10-14T12:00:00Z",
            "items": [
                {
                    "item_id": "P001288",
                    "amount": 20
                }
            ]
        }

        self.client.headers = {"API_KEY": "a1b2c3d4e5", "content-type": "application/json"}

    # Test to create a transfer using POST
    def test_1_post_transfer(self):
        response = self.client.post(self.baseUrl, json=self.test_body)
        self.assertEqual(response.status_code, 201)

    # Test to get all transfers using GET
    def test_2_get_transfers(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_id_exists(body, 119241))  # Checking the newly created ID 119241

    # Test to get a single transfer by ID using GET
    def test_3_get_transfer_by_id(self):
        response = self.client.get(f"{self.baseUrl}/119241")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("id"), 119241)
        self.assertEqual(body.get("reference"), "TR119241")
        self.assertEqual(body.get("transfer_to"), 9200)

    # Test to update a transfer using PUT
    def test_4_put_transfer(self):
        response = self.client.put(f"{self.baseUrl}/119241", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Fetch the updated transfer
        response = self.client.get(f"{self.baseUrl}/119241")
        body = response.json()
        self.assertEqual(body.get("transfer_to"), 9201)
        self.assertEqual(body.get("transfer_status"), "In Progress")
        self.assertTrue(match_date(body.get('updated_at'), date.today()))

    # Test to delete a transfer using DELETE
    def test_5_delete_transfer(self):
        response = self.client.delete(f"{self.baseUrl}/119241")
        self.assertEqual(response.status_code, 200)

        # Verify it was deleted
        response = self.client.get(self.baseUrl)
        self.assertFalse(check_id_exists(response.json(), 119241))

    # Test unauthorized access by removing the API key
    def test_6_unauthorized(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
