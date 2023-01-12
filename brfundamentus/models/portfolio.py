from brfundamentus.models.share import Share
from brfundamentus.models.stock_market import StockMarket
from brfundamentus.builders.portfolio_builder import build_list_of_shares
from brfundamentus.builders.trademap_builder import build_shares_from_trademap_info


class Portfolio:
    """
    Class to model a portfolio
    """

    def __init__(self, shares: list[Share]):
        self.shares = shares

    @property
    def total_invested(self):
        return sum(st.total_invested for st in self.shares)

    @property
    def equity(self):
        return sum(st.total_amount for st in self.shares)

    @property
    def return_of_investiment(self):
        return self.equity/self.total_invested - 1

    @classmethod
    def read_from_cvs(cls, path: str, market: StockMarket, sep: str = ','):
        with open(path) as file:
            all_info = file.readlines()

        all_stocks = build_list_of_shares(
            market=market, csv_info=all_info[1:], headers=all_info[0].split(sep))
        portfolio = Portfolio(all_stocks)

        return portfolio

    @classmethod
    def read_from_trademap_csv(cls, path: str, market: StockMarket, sep: str = ';'):
        with open(path) as file:
            all_info = file.readlines()

        all_stocks = build_shares_from_trademap_info(
            market=market, csv_info=all_info[1:], headers=all_info[0].split(sep))
        portfolio = Portfolio(all_stocks)
        breakpoint()
        portfolio.prune_shares()

        return portfolio

    def summary(self):
        print("Portfolio Summary\n\n")
        for st in self.shares:
            st.summary()
            self.print_share_info_in_portfolio(st)
            print("\n")

    def compute_share_position(self, share: Share):
        return round(100*(share.total_amount/self.equity), 2)

    def print_share_info_in_portfolio(self, share: Share):
        print(">Portfolio info")
        position = self.compute_share_position(share)
        print(
            f"Quantity: {share.quantity}\tTotal amount: {share.total_amount}\tPosition in portfolio: {position}")

    
    def prune_shares(self):
        self.shares = [share for share in self.shares if share.quantity != 0]

    def get_share_by_ticker(self, ticker:str):
        return next((share for share in self.shares if share.stock.ticker == ticker.upper()), None)
        
    def __repr__(self) -> str:
        msg = f"Portfolio with {len(self.shares)} shares\n"
        for share in self.shares:
            msg += str(share.quantity) + " " + share.stock.ticker + ", "
        return msg[:-2]