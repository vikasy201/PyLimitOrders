from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.orders: list[tuple[str, int, float, bool]] = []

    def add_order(self, buy: bool, product_id: str, amount: int, limit_price: float):
        self.orders.append((product_id, amount, limit_price, buy))

    def execute_orders(self, product_id: str, current_price: float):
        executed_orders = []
        for order in self.orders:
            if order[0] == product_id:
                if order[3]:  # buy order
                    if current_price <= order[2]:
                        self.execution_client.buy(order[0], order[1], order[2])
                        executed_orders.append(order)
                else:  # sell order
                    if current_price >= order[2]:
                        self.execution_client.sell(order[0], order[1], order[2])
                        executed_orders.append(order)
        for order in executed_orders:
            self.orders.remove(order)


    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        if product_id == "IBM" and price < 100:
            self.execution_client.buy("IBM", 1000, price)
