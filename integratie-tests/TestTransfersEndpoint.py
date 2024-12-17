import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists


class TestTransfersResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/transfers/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 119244
        self.ref = "TR119244"

        self.TEST_BODY = {
            "id": self.TEST_ID,
            "reference": "TR119244",
            "transfer_from": None,
            "transfer_to": 9200,
            "transfer_status": "Scheduled",
            "is_deleted": False,
            "items": [
                {
                    "item_id": "P001288",
                    "amount": 15
                }
            ]
        }

        self.ToPut = {
            "transfer_from": 9200,
            "transfer_to": 9201,
            "transfer_status": "In Progress",
        }

    # Test to create a transfer using POST
    def test_1_post_transfer(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 200)

    # Test to get all transfers using GET
    def test_2_get_transfers(self):
        response = self.client.get(self.baseUrl)
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body), 100)

    # Test to get a single transfer by ref using GET
    def test_3_get_transfer_by_id(self):
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("id"), self.TEST_ID)
        self.assertEqual(body.get("reference"), self.ref)
        self.assertEqual(body.get("transfer_to"), 9200)

    # Test to update a transfer using PUT
    def test_4_put_transfer(self):
        response = self.client.put(f"{self.baseUrl}{self.TEST_ID}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Fetch the updated transfer
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()
        self.assertEqual(body.get("transfer_from"), 9200)
        self.assertEqual(body.get("transfer_to"), 9201)
        self.assertEqual(body.get("transfer_status"), "In Progress")
        self.assertTrue(match_date(body.get('updated_at'), date.today()))

    # Test to delete a transfer using DELETE
    def test_5_delete_transfer(self):
        response = self.client.delete(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 200)

        # Verify it was deleted
        response = self.client.get(self.baseUrl)
        self.assertFalse(check_id_exists(response.json(), self.TEST_ID))

    # Test unauthorized access by removing the API key
    def test_6_no_apikey(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 422)

    def test_6_wrong_apikey(self):
        self.client.headers = {"api-key": "onzin", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
