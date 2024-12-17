import unittest
from httpx import Client
from datetime import date
from test_utils import match_date, check_id_exists, check_code_exists


class TestWarehouseResource(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://127.0.0.1:3000/api/v2/warehouses/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5", "content-type": "application/json"}

        self.TEST_ID = 99999  # deze is irrelevant, want ID wordt ge increment
        self.TEST_CODE = "TESTWARE"

        self.TEST_BODY = {
            "id": self.TEST_ID,
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
            "updated_at": "2010-04-26 18:16:09",
            "is_deleted": False
        }

        self.ToPut = {
            "address": "Wijnhaven 107",
            "city": "Rotterdam",
            "province": "Zuid-holland",
            "country": "NL"
        }

    # genummerd omdat volgorde van executie alfabetisch gaat

    def test_1_post_warehouse(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("code"), self.TEST_BODY["code"])
        self.assertEqual(response.json().get("name"), self.TEST_BODY["name"])
        # POST moet ook body teruggeven met gemaakte resource:
        # self.assertEqual(response.json().get("name"), self.TEST_BODY["name"])

    def test_1_post_warehouse_integrity_error(self):
        response = self.client.post(self.baseUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 400)
        self.assertIn("exists", response.json().get("detail"))

    def test_2_get_warehouses(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(check_code_exists(body, self.TEST_CODE))

    def test_3_get_warehouse_by_code(self):
        response = self.client.get(f"{self.baseUrl}?code={self.TEST_CODE}")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        # check of body klopt
        self.assertEqual(body.get("code"), self.TEST_CODE)
        self.assertEqual(body.get("name"), "test warehouse")
        self.assertEqual(body.get("city"), "testcity")

    def test_3_get_warehouse_notfound(self):
        response = self.client.get(f"{self.baseUrl}?code=non-existing-code")
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", body.get("detail"))

    def test_4_put_warehouse(self):
        response = self.client.put(f"{self.baseUrl}{self.TEST_CODE}", json=self.ToPut)

        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"{self.baseUrl}?code={self.TEST_CODE}")
        body = response.json()
        self.assertEqual(body.get('country'), 'NL')
        self.assertEqual(body.get('province'), 'Zuid-holland')
        self.assertEqual(body.get('city'), 'Rotterdam')
        self.assertEqual(body.get('address'), 'Wijnhaven 107')

        self.assertTrue(match_date(body.get('updated_at'), date.today()))

    def test_4_put_warehouse_notfound(self):
        response = self.client.put(f"{self.baseUrl}non-existing-code", json=self.ToPut)
        body = response.json()
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", body.get("detail"))

    def test_5_delete_warehouse(self):
        # teardown/cleanup
        response = self.client.delete(f"{self.baseUrl}{self.TEST_CODE}")

        self.assertEqual(response.status_code, 200)

        na_delete = self.client.get(self.baseUrl)
        # check of deleted
        self.assertFalse(check_code_exists(na_delete.json(), self.TEST_CODE))

    # alle locations met warehouse_id 1
    # afhankelijk per endpoint of deze optie bestaat; zie endpoint documentatie
    """
    def test_6_get_warehouse_locations(self):
        response = self.client.get(f"{self.baseUrl}/1/locations")
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body[0].get("warehouse_id"), 1)
    """

    def test_6_no_api_key(self):
        self.client.headers = {"content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 422)
    
    def test_7_wrong_api_key(self):
        self.client.headers = {"api-key": "randomguess", "content-type": "application/json"}
        response = self.client.get(self.baseUrl)

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
