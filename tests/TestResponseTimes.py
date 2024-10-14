import unittest
from test_utils import get_response_time


class TestResponseTimes(unittest.TestCase):
    # hiervoor alleen de grootste files gebruiken, voor langst mogelijke tijden
    def setUp(self):
        self.shipmentsUrl = "http://localhost:3000/api/v1/shipments"
        self.ordersUrl = "http://localhost:3000/api/v1/orders"
        self.transfersUrl = "http://localhost:3000/api/v1/transfers"
        self.inventoriesUrl = "http://localhost:3000/api/v1/inventories"

    def test_1_Shipments_time(self):
        resp_time = get_response_time(self.shipmentsUrl)
        self.assertLess(resp_time, 200, f"""Response tijd voor GET shipments: {
                        resp_time:.2f}ms, te langzaam.""")

    def test_2_Orders_time(self):
        resp_time = get_response_time(self.ordersUrl)
        self.assertLess(resp_time, 200, f"""Response tijd voor GET orders: {
                        resp_time:.2f}ms, te langzaam.""")

    def test_3_Transfers_time(self):
        resp_time = get_response_time(self.transfersUrl)
        self.assertLess(resp_time, 200, f"""Response tijd voor GET transfers: {
                        resp_time:.2f}ms, te langzaam.""")

    def test_4_Inventories_time(self):
        resp_time = get_response_time(self.inventoriesUrl)
        self.assertLess(resp_time, 200, f"""Response tijd voor GET inventories: {
                        resp_time:.2f}ms, te langzaam.""")


if __name__ == '__main__':
    unittest.main()
