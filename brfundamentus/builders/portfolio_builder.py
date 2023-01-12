from brfundamentus.models.stock_market import StockMarket
from brfundamentus.models.share import Share
from brfundamentus.utils.utils import parse_str_to_float


def build_single_share(market: StockMarket,  headers: list[str], info: list[str]):
    """
    Build a single share for a portfolio
    """

    map_info = {parameter.strip().upper(): info[idx]
                for idx, parameter in enumerate(headers)}

    stock = market.get_stock_by_ticker(map_info['TICKER'])

    return Share(stock=stock,
                 mean_price=parse_str_to_float(map_info['PRECO MEDIO']),
                 quantity=int(parse_str_to_float(map_info['QTD'])))


def build_list_of_shares(market: StockMarket, csv_info: list[str], headers: list[str]):
    """
    Build a list of StockInPortfolio from a csv file
    """

    shares = list()
    for line in csv_info:
        splited = line.split(',')
        stock = build_single_share(market, headers, splited)
        shares.append(stock)

    return shares
