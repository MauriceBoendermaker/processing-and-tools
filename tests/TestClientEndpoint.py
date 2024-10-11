import unittest
from httpx import Client
from test_utils import match_date, check_id_exists
from datetime import date


class TestClientEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/clients"
        self.client = Client()

        self.test_body = {
            "id": 9821,
            "name": "test client",
            "address": "Carstenallee 2",
            "city": "Herzberg",
            "zip_code": "89685",
            "province": "Niedersachsen",
            "country": "Germany",
            "contact_name": "Ing. Ferdi Steckel MBA.",
            "contact_phone": "+49(0)5162 147719",
            "contact_email": "conradikati@example.net",
            "created_at": "1995-06-09 13:13:02",
            "updated_at": "2022-09-13 19:15:30"
        }

        self.ToPut = {
            "id": 9821,
            "name": "test client",
            "address": "Wijnhaven 107",
            "city": "Rotterdam",
            "zip_code": "89685",
            "province": "Niedersachsen",
            "country": "Germany",
            "contact_name": "Ing. Ferdi Steckel MBA.",
            "contact_phone": "+49(0)5162 147719",
            "contact_email": "conradikati@example.net",
            "created_at": "1995-06-09 13:13:02",
            "updated_at": "2022-09-13 19:15:30"
        }

        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}

    # genummerd omdat volgorde van executie alfabetisch gaat
    def test_1_post_client(self):
        response = self.client.post(self.baseUrl, json=self.test_body)

        self.assertEqual(response.status_code, 201)

        # in de toekomst moet POST ook body teruggeven met gemaakte resource:
        # self.assertEqual(response.json().get("name"), "test client")

    def test_2_get_clients(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(check_id_exists(body, 9821), True)

    def test_3_get_client(self):
        response = self.client.get(f"{self.baseUrl}/9821")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        # check of body klopt
        self.assertEqual(body.get("id"), 9821)
        self.assertEqual(body.get("name"), "test client")
        self.assertEqual(body.get("address"), "Carstenallee 2")
        self.assertEqual(body.get("city"), "Herzberg")

    def test_4_put_client(self):
        response = self.client.put(
            f"{self.baseUrl}/9821", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}/9821")
        body = response.json()

        self.assertEqual(body.get('address'), 'Wijnhaven 107')
        self.assertEqual(body.get('city'), 'Rotterdam')
        self.assertTrue(match_date(body.get('updated_at'), date.today()))

    def test_5_delete_client(self):
        # teardown/cleanup
        response = self.client.delete(f"{self.baseUrl}/9821")

        self.assertEqual(response.status_code, 200)

        na_delete = self.client.get(self.baseUrl)
        self.assertFalse(check_id_exists(na_delete.json(), 9821))

    # alle orders met ship_to en bill_to 1 (de juiste client)
    # afhankelijk per endpoint of deze optie bestaat, zie endpoint documentatie
    def test_6_get_client_orders(self):
        response = self.client.get(f"{self.baseUrl}/1/orders")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body[0].get("ship_to"), 1)
        self.assertEqual(body[0].get("bill_to"), 1)

    def test_7_unauthorized(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
