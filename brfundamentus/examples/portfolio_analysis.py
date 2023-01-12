from brfundamentus.models.stock_market import StockMarket
from brfundamentus.models.portfolio import Portfolio


path_to_data = "./statusinvest-busca-avancada.csv"
path_to_portfolio = "./portfolio.csv"
path_to_trademap = "./transacoes.csv"

market = StockMarket.read_from_csv(path_to_data)
portfolio = Portfolio.read_from_cvs(path_to_portfolio, market)
portfolio.summary()
