from brfundamentus.models.stock import Stock
from brfundamentus.utils.utils import compute_greenblatt_rank
from brfundamentus.builders.stock_builder import build_list_of_stocks


class StockMarket:
    """
    This class is responsible to handle fundamentalist information
    about the shares in the market
    """

    def __init__(self, stocks: list[Stock]):
        self.stocks = stocks
        compute_greenblatt_rank(self.stocks)

    def get_stock_by_ticker(self, ticker: str):
        return next(
            (stock for stock in self.stocks if stock.ticker == ticker.upper()),
            None,
        )

    @classmethod
    def read_from_csv(cls, path: str, market_risk: float = 0.15):
        with open(path) as file:
            all_info = file.readlines()

        all_stocks = build_list_of_stocks(
            all_info[1:], all_info[0].split(';'), market_risk
        )
        market = StockMarket(all_stocks)

        return market

    def __filter_stocks_by_single_criterion(
        self,
        parameter: str,
        cut_criterion: float = 0,
        reverse_cut: bool = False,
        disconsider: list = None,
        only_from: list = None,
    ) -> list[Stock]:

        if disconsider is None:
            disconsider = []
        if only_from is None:
            only_from = []

        if parameter not in list(self.stocks[0].__dict__.keys()):
            return []

        modifier = -1 if reverse_cut else 1
        stocks_list = [
            stock
            for stock in self.stocks
            if stock.__dict__[parameter] is not None
            and stock.ticker not in disconsider
            and modifier * stock.__dict__[parameter] > modifier * cut_criterion
            and stock.ticker not in disconsider
        ]

        if only_from:
            stocks_list = [
                stock for stock in stocks_list if stock.ticker in only_from
            ]

        return stocks_list

    def get_top_stocks_by_criterion(
        self,
        num_stocks: int,
        parameter: str,
        cut_criterion: float = 0,
        reverse_cut: bool = False,
        ascending: bool = False,
        disconsider: list = None,
        only_from: list = None,
    ) -> list[Stock]:
        """
        This method filter stocks by a given criterion.
        Returns a list of dictionaries with all information of the filterd stocks.
        Parameters:
            - num_stocks (int): Maximum lenght of the result list.
            - parameter (string): The parameter by which we want to filter the stocks.
                                It should be a key from the dictionary of all info. Otherwise, method will return a empty list.
            - cut_criterion (float): Value used as cut criterion. Default value is 0.
                                    By default, method selects all stocs which 'parameter' value is grether then 'cut_criterion'
            - reverse_cut (bool): If True, method will invert the condiction, selecting all stocs which 'parameter' value is less then 'cut_criterion'.
                                Default value is False.
            - ascending (bool): If True, result list will be sorted by ascending values of 'parameter'.
                                If Falae, result list will be sorted by descending values of 'parameter'.
                                Default value is False.
            - disconsider (list): A list of tickers. All stocks with thoses tickers will be excluded in the final result.
            - only_from (list): A list of tickers. Method will only consider stocks from that list before filter by given criterion.
        """

        stocks_list = self.__filter_stocks_by_single_criterion(
            parameter=parameter,
            cut_criterion=cut_criterion,
            reverse_cut=reverse_cut,
            disconsider=disconsider,
            only_from=only_from,
        )

        stocks_list.sort(
            key=lambda st: st.__dict__[parameter], reverse=not ascending
        )

        max_index = min(num_stocks, len(stocks_list))

        return stocks_list[:max_index]

    def get_top_stocks_by_list_of_conditions(
        self,
        conditions: list[dict],
        sort_by: dict,
        num_stocks: int = 50,
        disconsider: list = None,
        only_from: list = None,
    ) -> list[Stock]:
        """
        This method filter the stocsk by a list of criteria.
        Returns a list of dictionaries with all information of the filterd stocks.
        Params:
            - conditions: A list of dictionaries, each one containing information of one criterion.
                            Each dictionarie must have the following keys:
                                - 'parameter' (string): the criterion one wants to filter. Should be a key from the dictionarie of all info.
                                - 'cut_criterion' (float): a value used as cut criterion.
                                - 'reverse_cut' (bool): flag to indicate if the cut_criterion is reversed.
            -sort_by: A dictionary to indicate for what parameter we must sort the results.
                        This dictionary must have the follwing keys:
                            - 'parameter': for which we sort by
                            - 'ascending': True if sort ascending, False otherwise
            - num_stocks (int): Maximum number of stocks in the result list. Default value is 50.
            - disconsider (list): A list of tickers. All stocks with thoses tickers will be excluded in the final result.
            - only_from (list): A list of tickers. Method will only consider stocks from that list before filter by given criterion.
        """

        list_of_stocks_filtered = list()
        for criterion in conditions:
            total_stocks = self.__filter_stocks_by_single_criterion(
                parameter=criterion['parameter'],
                cut_criterion=criterion['cut_criterion'],
                reverse_cut=criterion['reverse_cut'],
                disconsider=disconsider,
                only_from=only_from,
            )

            list_of_stocks_filtered.append(total_stocks)

        selected_stocks = [
            stock
            for stock in self.stocks
            if all(
                (
                    stock in single_list
                    for single_list in list_of_stocks_filtered
                )
            )
        ]

        selected_stocks.sort(
            key=lambda st: st.__dict__[sort_by['parameter']],
            reverse=not sort_by['ascending'],
        )

        limit = min(len(selected_stocks), num_stocks)

        return selected_stocks[:limit]


if __name__ == '__main__':
    file_path = './statusinvest-busca-avancada.csv'

    # teste get stock
    market = StockMarket.read_from_csv(file_path)
    b3 = market.get_stock_by_ticker('B3SA3')

    # test get top 10 by criterion
    print(
        b3.greenblatt_rank,
        b3.gordon_valuation,
        b3.graham_valuation,
        b3.bazin_valuation,
    )
    selected_stocks = market.get_top_stocks_by_criterion(10, 'dy')
    print(selected_stocks)

    # test get top 10 by list of criteria
    criteria = [
        {'parameter': 'dy', 'cut_criterion': 0.03, 'reverse_cut': False},
        {
            'parameter': 'net_margin',
            'cut_criterion': 0.15,
            'reverse_cut': False,
        },
    ]

    sort_by = {'parameter': 'roe', 'ascending': True}

    selected_stocks = market.get_top_stocks_by_list_of_conditions(
        conditions=criteria, sort_by=sort_by, num_stocks=10
    )
    print(selected_stocks)
