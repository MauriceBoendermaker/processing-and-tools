import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists


class TestClientResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v2/clients/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 9821

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
            "contact_email": "conradikati@example.net",
            "is_deleted": False
        }

        self.ToPut = {
            "address": "Wijnhaven 107",
            "city": "Rotterdam"
        }

    # genummerd omdat volgorde van executie alfabetisch gaat
    def test_1_post_client(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)

        self.assertIn(response.status_code, [200, 201])

        # in de toekomst moet POST ook body teruggeven met gemaakte resource:
        # self.assertEqual(response.json().get("name"), self.TEST_BODY["name"])

    def test_2_get_clients(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(check_id_exists(body, self.TEST_ID))#dqwqwdqwdqwd

    def test_3_get_client(self):
        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        # check of body klopt
        self.assertEqual(body.get("id"), self.TEST_ID)
        self.assertEqual(body.get("name"), "test client")
        self.assertEqual(body.get("address"), "Carstenallee 2")
        self.assertEqual(body.get("city"), "Herzberg")

    def test_4_put_client(self):
        response = self.client.put(
            f"{self.baseUrl}{self.TEST_ID}", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?id={self.TEST_ID}")
        body = response.json()

        self.assertEqual(body.get('address'), 'Wijnhaven 107')
        self.assertEqual(body.get('city'), 'Rotterdam')
        self.assertTrue(match_date(body.get('updated_at'), date.today()))

    def test_5_delete_client(self):
        # teardown/cleanup
        response = self.client.delete(f"{self.baseUrl}{self.TEST_ID}")

        self.assertEqual(response.status_code, 200)

        na_delete = self.client.get(self.baseUrl)
        # check of deleted
        self.assertFalse(check_id_exists(na_delete.json(), self.TEST_ID))

    # alle orders met ship_to en bill_to 1 (de juiste client)
    # afhankelijk per endpoint of deze optie bestaat, zie endpoint documentatie
    """
    def test_6_get_client_orders(self):
        response = self.client.get(f"{self.baseUrl}1/orders")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body[0].get("ship_to"), 1)
        self.assertEqual(body[0].get("bill_to"), 1)
    """

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
