import unittest
from httpx import Client
from test_utils import match_date, check_id_exists
from datetime import date


class TestWarehouseResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/warehouses"
        self.client = Client()

        self.test_body = {
            "id": 59,
            "code": "TESTWARE",
            "name": "test warehouse",
            "address": "Gabriele-Junken-Ring 5/1",
            "zip": "35100",
            "city": "testcity",
            "province": "Brandenburg",
            "country": "DE",
            "contact": {
                "name": "Bozena Steckel",
                "phone": "(08587) 18542",
                "email": "adolfinehentschel@example.net"
            },
            "created_at": "2006-08-31 03:38:40",
            "updated_at": "2010-04-26 18:16:09"
        }

        self.ToPut = {
            "id": 59,
            "code": "TESTWARE",
            "name": "test warehouse",
            "address": "Wijnhaven 107",
            "zip": "35100",
            "city": "Rotterdam",
            "province": "Zuid-holland",
            "country": "NL",
            "contact": {
                "name": "Bozena Steckel",
                "phone": "(08587) 18542",
                "email": "adolfinehentschel@example.net"
            },
            "created_at": "2006-08-31 03:38:40",
            "updated_at": "2010-04-26 18:16:09"
        }

        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}

    # genummerd omdat volgorde van executie alfabetisch gaat
    def test_1_post_warehouse(self):
        response = self.client.post(self.baseUrl, json=self.test_body)

        self.assertEqual(response.status_code, 201)

        # in de toekomst moet POST ook body teruggeven met gemaakte resource:
        # self.assertEqual(response.json().get("name"), self.test_body["name"])

    def test_2_get_warehouses(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_id_exists(body, 59))

    def test_3_get_warehouse(self):
        response = self.client.get(f"{self.baseUrl}/59")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        # check of body klopt
        self.assertEqual(body.get("id"), 59)
        self.assertEqual(body.get("code"), "TESTWARE")
        self.assertEqual(body.get("name"), "test warehouse")
        self.assertEqual(body.get("city"), "testcity")

    def test_4_put_warehouse(self):
        response = self.client.put(
            f"{self.baseUrl}/59", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}/59")
        body = response.json()
        self.assertEqual(body.get('country'), 'NL')
        self.assertEqual(body.get('province'), 'Zuid-holland')
        self.assertEqual(body.get('city'), 'Rotterdam')
        self.assertEqual(body.get('address'), 'Wijnhaven 107')

        self.assertTrue(match_date(body.get('updated_at'), date.today()))

    def test_5_delete_warehouse(self):
        # teardown/cleanup
        response = self.client.delete(f"{self.baseUrl}/59")

        self.assertEqual(response.status_code, 200)

        na_delete = self.client.get(self.baseUrl)
        # check of deleted
        self.assertFalse(check_id_exists(na_delete.json(), 59))

    # alle locations met warehouse_id 1
    # afhankelijk per endpoint of deze optie bestaat; zie endpoint documentatie
    def test_6_get_warehouse_locations(self):
        response = self.client.get(f"{self.baseUrl}/1/locations")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body[0].get("warehouse_id"), 1)

    def test_7_unauthorized(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
