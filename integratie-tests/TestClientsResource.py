import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists


class TestClientResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/clients/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 9837

        self.TEST_BODY = {
            "id": self.TEST_ID,
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
        self.assertIn(response.status_code, [200, 201])

        # Verify the resource was created
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("id"), self.TEST_ID)

    def test_2_get_clients(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(check_id_exists(body, self.TEST_ID))

    def test_3_get_client(self):
        # Ensure the client exists before retrieving
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body.get("id"), self.TEST_ID)
        self.assertEqual(body.get("name"), self.TEST_BODY["name"])
        self.assertEqual(body.get("address"), self.TEST_BODY["address"])
        self.assertEqual(body.get("city"), self.TEST_BODY["city"])

    def test_4_put_client(self):
        # Update the client details
        response = self.client.put(f"{self.baseUrl}{self.TEST_ID}", json=self.ToPut)
        self.assertEqual(response.status_code, 200)

        # Verify the updated details
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()

        self.assertEqual(body.get("address"), self.ToPut["address"])
        self.assertEqual(body.get("city"), self.ToPut["city"])


    def test_5_delete_client(self):
        # Delete the client
        response = self.client.delete(f"{self.baseUrl}{self.TEST_ID}")
        self.assertEqual(response.status_code, 200)

        # Verify the client is deleted
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        self.assertEqual(response.status_code, 404)

    def test_7_no_apikey(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 422)

    def test_7_wrong_apikey(self):
        self.client.headers = {"api-key": "onzin", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()