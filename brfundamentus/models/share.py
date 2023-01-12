from brfundamentus.models.stock import Stock
from brfundamentus.models.operation import Operation, OperationType
from brfundamentus.utils.utils import round_value as rv


class Share:
    """
    Class to model a stock inside a portfolio
    """

    def __init__(self, stock: Stock, mean_price: float, quantity: int):
        self.stock: Stock = stock
        self.mean_price: float = mean_price
        self.quantity: int = quantity
        self.operations_history: list[Operation] = list()

        self.__fill_first_buy()

    @property
    def total_invested(self):
        return self.quantity * self.mean_price

    @property
    def return_of_investiment(self):
        return self.stock.price / self.mean_price - 1

    @property
    def total_amount(self):
        return self.quantity * self.stock.price

    def __fill_first_buy(self):
        operation = Operation(
            ticker=self.stock.ticker,
            price=self.mean_price,
            quantity=self.quantity,
            type=OperationType.BUY,
        )
        self.operations_history.append(operation)

    def print_investiment_info(self):
        print(
            f'{self.mean_price} | {self.stock.price} | {self.return_of_investiment}'
        )
        self.stock.print_valuations()

    def __compute_new_mean_price(self, price: float, num_stocks: int):
        self.mean_price = round(
            (self.quantity * self.mean_price + price * num_stocks)
            / (num_stocks + self.quantity),
            2,
        )

    def buy(self, price: float, num_stocks: int):
        self.__compute_new_mean_price(price, num_stocks)
        self.quantity += num_stocks
        operation = Operation(
            ticker=self.stock.ticker,
            price=price,
            quantity=num_stocks,
            type=OperationType.BUY,
        )
        self.operations_history.append(operation)

    def sell(self, price, num_stocks):
        self.quantity -= num_stocks
        operation = Operation(
            ticker=self.stock.ticker,
            price=price,
            quantity=num_stocks,
            type=OperationType.SELL,
        )
        self.operations_history.append(operation)

    def summary(self):
        up_down = 'Upside' if self.return_of_investiment > 0 else 'Downside'
        print(f'>>> Ticker: {self.stock.ticker}\n>General info')
        print(
            f'Actual Price: {self.stock.price}\tMean Price: {self.mean_price}\t{up_down}: {rv(self.return_of_investiment)}'
        )
        print('>Valuation info')
        print(
            f'Graham: {rv(self.stock.graham_valuation)}\tBazin: {rv(self.stock.bazin_valuation)}\tGordon: {rv(self.stock.gordon_valuation)}'
        )
        print('>Other info')
        print(
            f'Greenblatt: {self.stock.greenblatt_rank}\tAverage Growth: {rv(self.stock.average_growth)}\tDivided Yield: {rv(self.stock.dy)}'
        )

    def __repr__(self) -> str:
        return f'{self.quantity} shares of {self.stock.ticker}, mean price {self.mean_price}'
