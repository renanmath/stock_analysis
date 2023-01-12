from brfundamentus.models.share import Share
from brfundamentus.models.stock_market import StockMarket
from brfundamentus.utils.utils import parse_str_to_float
from pydantic.error_wrappers import ValidationError

"""
Builds shares from TradeMap csv file of transactions
"""


def build_single_share_from_trademap_info(market: StockMarket,
                                          headers: list[str],
                                          info: list[str],
                                          map_of_shares: dict[str, Share]):

    map_info = {parameter.strip().upper(): info[idx]
                for idx, parameter in enumerate(headers)}

    stock = market.get_stock_by_ticker(map_info['ATIVO'])
    if stock is None:
        return
    if stock.ticker in map_of_shares:
        compute_transaction(share=map_of_shares[stock.ticker],
        operation=map_info['OPERAÇÃO'].upper(),
        quantity=int(parse_str_to_float(map_info['QUANTIDADE'])),
        price=parse_str_to_float(map_info['PREÇO'])
        )
    else:
        share = Share(stock=stock,
                mean_price=parse_str_to_float(map_info['PREÇO']),
                quantity=int(parse_str_to_float(map_info['QUANTIDADE'])))
        map_of_shares[stock.ticker] = share
    


def compute_transaction(share: Share, operation: str, quantity: int, price: float):
    if operation == 'COMPRA':
        share.buy(price=price, num_stocks=quantity)
    elif operation == 'VENDA':
        share.sell(price=price, num_stocks=quantity)
    else:
        return None


def build_shares_from_trademap_info(market: StockMarket, csv_info: list[str], headers: list[str]):
    map_of_shares = dict()
    for line in csv_info:
        splited = line.split(';')
        try:
            build_single_share_from_trademap_info(market, headers, splited, map_of_shares)
        except ValidationError:
            print(splited)
            continue

    shares = list(map_of_shares.values())
    return shares

