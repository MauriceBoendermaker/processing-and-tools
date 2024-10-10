import unittest
from httpx import Client


def check_id_exists(json, target_id):
    for item in json:
        if item["id"] == target_id:
            return True
    return False


class TestWarehouseEndpoint(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://localhost:3000/api/v1/warehouses"
        self.client = Client()
        self.test_body = {
            "id": 56,
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
            "id": 1,
            "code": "YQZZNL56",
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Heemskerk",
            "province": "Friesland",
            "country": "BE",
            "contact": {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "1983-04-13 04:59:55",
            "updated_at": "2024-10-08T13:28:19.911773Z"
        }

        self.client.headers = {"API_KEY": "a1b2c3d4e5",
                               "content-type": "application/json"}
    # genummerd omdat volgorde van executie alfabetisch gaat

    def test_1_post_warehouse(self):
        response = self.client.post(self.baseUrl, json=self.test_body)

        self.assertEqual(response.status_code, 201)

    def test_2_get_warehouses(self):
        response = self.client.get(self.baseUrl)
        body = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(check_id_exists(body, 56), True)

    def test_3_get_warehouse(self):
        response = self.client.get(f"{self.baseUrl}/1")

        self.assertEqual(response.status_code, 200)

    def test_4_delete_warehouse(self):
        response = self.client.delete(self.baseUrl + "/56")

        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            self.assertEqual(check_id_exists(
                self.client.get(self.baseUrl).json(), "56"), False)

    def test_5_put_warehouse(self):
        response = self.client.put(
            self.baseUrl + "/1", json=self.ToPut)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), )

        response = self.client.get(f"{self.baseUrl}/1")
        body = response.json()
        self.assertEqual(body.get('country'), 'BE')

        # cleanup
        self.ToPut['country'] = 'NL'
        self.client.put(
            self.baseUrl + "/1", json=self.ToPut)


if __name__ == '__main__':
    unittest.main()
