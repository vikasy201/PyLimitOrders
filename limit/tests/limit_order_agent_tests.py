import unittest
from unittest.mock import MagicMock
from limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.execution_client = ExecutionClient()
        self.agent = LimitOrderAgent(self.execution_client)

    def test_on_price_tick_buy_IBM(self):
        self.agent.on_price_tick("IBM", 99)
        self.execution_client.buy.assert_called_once_with("IBM", 1000, 99)

    def test_add_order(self):
        self.agent.add_order(True, "IBM", 500, 98)
        self.agent.add_order(False, "AAPL", 200, 120)
        self.assertEqual(len(self.agent.orders), 2)
        self.assertEqual(self.agent.orders[0], ("IBM", 500, 98, True))
        self.assertEqual(self.agent.orders[1], ("AAPL", 200, 120, False))

    def test_execute_orders_buy(self):
        self.agent.add_order(True, "IBM", 500, 98)
        self.agent.add_order(True, "IBM", 700, 97)
        self.agent.on_price_tick("IBM", 96)
        self.execution_client.buy.assert_not_called()

        self.agent.on_price_tick("IBM", 98)
        self.execution_client.buy.assert_called_once_with("IBM", 500, 98)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0], ("IBM", 700, 97, True))

    def test_execute_orders_sell(self):
        self.agent.add_order(False, "IBM", 500, 102)
        self.agent.add_order(False, "IBM", 700, 103)
        self.agent.on_price_tick("IBM", 104)
        self.execution_client.sell.assert_not_called()

        self.agent.on_price_tick("IBM", 102)
        self.execution_client.sell.assert_called_once_with("IBM", 500, 102)
        self.assertEqual(len(self.agent.orders), 1)
        self.assertEqual(self.agent.orders[0], ("IBM", 700, 103, False))

if __name__ == "__main__":
    unittest.main()