import unittest
from httpx import Client, HTTPStatusError
from datetime import date
from test_utils import match_date_timezone, check_id_exists


class TestOrderResource(unittest.TestCase):
    def setUp(self):
        self.ordersUrl = "http://localhost:3000/api/v2/orders/"
        self.inventoriesUrl = "http://localhost:3000/api/v2/inventories/"
        self.client = Client()
        self.client.headers = {"api-key": "a1b2c3d4e5",
                               "Content-Type": "application/json"}

        self.ORDER_TEST_ID = 13348

        self.TEST_BODY = {
            "id": self.ORDER_TEST_ID,
            "source_id": 82,
            "order_date": "1995-05-27T20:02:30Z",
            "request_date": "1995-05-31T20:02:30Z",
            "reference": "ORD06490",
            "reference_extra": "Lorem ipsum dolor sit amet.",
            "order_status": "Pending",
            "notes": "Lorem ipsum dolor sit amet.",
            "shipping_notes": "Lorem ipsum dolor sit amet.",
            "picking_notes": "Lorem ipsum dolor sit amet.",
            "warehouse_id": 36,
            "ship_to": 5254,
            "bill_to": 3016,
            "shipment_id": [5555],  # 9006 voor delivered en O, 9102 goed
            "total_amount": 6070.46,
            "total_discount": 295.5,
            "total_tax": 388.58,
            "total_surcharge": 37.91,
            "is_deleted": False,
            "items": [
                {
                    "item_id": "P000001",
                    "amount": 7
                }
            ]
        }

    def test_1_order_input_validation(self):
        # probeert order met fout veld, en checkt voor 422
        self.TEST_BODY["order_status"] = "Invalid"
        response = self.client.post(self.ordersUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 422)

    def test_2_invalid_stock(self):
        self.TEST_BODY["order_status"] = "Pending"
        response = self.client.get(
            f"{self.inventoriesUrl}?item_reference=P000001")
        inven = response.json()
        self.assertEqual(response.status_code, 200)
        # pakt beschikbaar van een inventory, bestelt te veel.
        available = inven["total_available"]
        self.TEST_BODY["items"] = [{"item_id": f"{inven['item_id']}",
                                    "amount": available + 1}]

        response = self.client.post(self.ordersUrl, json=self.TEST_BODY)

        # checkt op 409 conflict en foutmelding
        self.assertEqual(response.status_code, 409)
        self.assertIn(
            f"only {available} available", response.json().get("detail"))

    def test_3_invalid_shipment_link(self):
        # eerst de andere velden juist maken, shipment_id nog fout

        response = self.client.post(self.ordersUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 409)
        self.assertIn(
            "cannot link order with an incoming shipment",
            response.json().get("detail"))
        # proberen te linken met shipment 5555, incoming
        self.TEST_BODY["shipment_id"].remove(5555)
        self.TEST_BODY["shipment_id"].append(9006)

        response = self.client.post(self.ordersUrl, json=self.TEST_BODY)
        self.assertEqual(response.status_code, 409)
        self.assertIn(
            "cannot link order with Delivered shipment",
            response.json().get("detail"))
        # proberen te linken met shipment 9006, Delivered
        self.TEST_BODY["shipment_id"].remove(9006)
        self.TEST_BODY["shipment_id"].append(9102)
        # deze klopt wel, voor de volgende

    def test_4_stock_after_order(self):
        # maar 1 bestellen, juiste shipment linken
        self.TEST_BODY["items"][0]["amount"] = 1
        self.TEST_BODY["shipment_id"].remove(5555)
        self.TEST_BODY["shipment_id"].append(9102)

        response_inventory_before = self.client.get(
            f"{self.inventoriesUrl}?item_reference=P000001")
        inven_before = response_inventory_before.json()

        response = self.client.post(self.ordersUrl, json=self.TEST_BODY)

        self.assertEqual(response.status_code, 200)

        response_inventory_after = self.client.get(
            f"{self.inventoriesUrl}?item_reference=P000001")
        inven_after = response_inventory_after.json()

        # checkt of voorraad is bijgewerkt na plaatsen van de order
        self.assertEqual(inven_before["total_available"] - 1,
                         inven_after["total_available"])
        self.assertEqual(inven_before["total_ordered"] + 1,
                         inven_after["total_ordered"])

    def test_5_order_status_change(self):
        update_response = self.client.put(
            f"{self.ordersUrl}{self.ORDER_TEST_ID}",
            json={"order_status": "Delivered"})
        self.assertEqual(update_response.status_code, 200)

        # Mag niet terug veranderd worden na Completed status
        invalid_update_response = self.client.put(
            f"{self.ordersUrl}{self.ORDER_TEST_ID}",
            json={"order_status": "Pending"})
        self.assertEqual(invalid_update_response.status_code, 403)
        self.assertIn("Unable to change order status back from Delivered",
                      invalid_update_response.json().get("detail"))

    # def test_6_monthly_report(self):
    #     report_response = self.client.get(
    #         "http://localhost:3000/api/v2/reports/?year_to_report=2025&month_to_report=1")
    #     # checkt of reporting werkt, statuscode/bericht/filename
    #     self.assertEqual(report_response.status_code, 200)
    #     self.assertIn("report PDF generated successfully.",
    #                   report_response.json().get("message"))
    #     self.assertIn("report_for_all_month_2025-1.pdf",
    #                   report_response.json().get("pdf_url"))

    #     # cleanup
    #     del_response = self.client.delete(
    #         f"{self.ordersUrl}{self.ORDER_TEST_ID}")
    #     self.assertEqual(del_response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
