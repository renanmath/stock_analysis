"""
Methods to build stocks and list of stocks
"""

from pydantic.error_wrappers import ValidationError
from brfundamentus.models.stock import Stock
from brfundamentus.utils.utils import parse_str_to_float
import math


def build_single_stock(
    info: list[str], headers: list[str], market_risk: float
) -> Stock:
    """
    Build a Stock from a list of strings
    """

    map_info = {
        parameter.strip(): info[idx] for idx, parameter in enumerate(headers)
    }

    ticker = map_info['TICKER']

    # basic indicators
    price = parse_str_to_float(map_info['PRECO'])
    dy = parse_str_to_float(map_info['DY'], 100)
    price_per_profit = parse_str_to_float(map_info['P/L'])
    price_to_book = parse_str_to_float(map_info['P/VP'])
    gross_margin = parse_str_to_float(map_info['MARGEM BRUTA'], 100)
    net_margin = parse_str_to_float(map_info['MARG. LIQUIDA'], 100)
    ebit_margin = parse_str_to_float(map_info['MARGEM EBIT'], 100)
    ev_per_ebit = parse_str_to_float(map_info['EV/EBIT'])
    current_liquidity = parse_str_to_float(map_info['LIQ. CORRENTE'])
    net_debt_to_equity = parse_str_to_float(map_info['DIV. LIQ. / PATRI.'])
    roe = parse_str_to_float(map_info['ROE'], 100)
    roa = parse_str_to_float(map_info['ROA'])
    roic = parse_str_to_float(map_info['ROIC'], 100)
    cagr = parse_str_to_float(map_info['CAGR LUCROS 5 ANOS'], 100)
    advt = parse_str_to_float(map_info['LIQUIDEZ MEDIA DIARIA'], 1000000)
    bvps = parse_str_to_float(map_info['VPA'])
    eps = parse_str_to_float(map_info['LPA'])
    book_value = parse_str_to_float(map_info['VALOR DE MERCADO'], 1000000000)

    # extra indicators
    dps = dy * price if dy is not None else None
    payout = (
        dps / eps if dps is not None and eps is not None and eps != 0 else None
    )

    if roe is None or payout is None:
        expected_growth = None
    else:
        expected_growth = (1 - payout) * roe if payout != 0 else 0.2 * roe

    average_growth = (
        expected_growth
        if cagr is None or expected_growth is None
        else (expected_growth + cagr) / 2
    )

    if (
        price_per_profit is None
        or average_growth is None
        or average_growth == 0
    ):
        peg = None
    else:
        peg = price_per_profit / average_growth

    # valiations

    fair_price_graham = (
        None
        if eps is None
        or bvps is None
        or eps * bvps < 0
        or eps < 0
        or price is None
        or price == 0
        else math.sqrt(22.5 * eps * bvps)
    )
    graham_valuation = (
        None if fair_price_graham is None else (fair_price_graham / price) - 1
    )

    fair_price_bazin = (
        None if dps is None or price is None or price == 0 else dps / 0.06
    )
    bazin_valuation = (
        None if fair_price_bazin is None else (fair_price_bazin / price) - 1
    )

    fair_price_gordon = (
        None
        if cagr is None or dps is None or price is None or price == 0
        else (1 / market_risk) * dps * (1 + 0.1 * cagr)
    )
    gordon_valuation = (
        None if fair_price_gordon is None else (fair_price_gordon / price) - 1
    )

    stock = Stock(
        ticker=ticker,
        price=price,
        dy=dy,
        roe=roe,
        roic=roic,
        roa=roa,
        eps=eps,
        price_to_book=price_to_book,
        gross_margin=gross_margin,
        net_margin=net_margin,
        ebit_margin=ebit_margin,
        current_liquidity=current_liquidity,
        net_debt_to_equity=net_debt_to_equity,
        ev_per_ebit=ev_per_ebit,
        bvps=bvps,
        price_per_profit=price_per_profit,
        cagr=cagr,
        adtv=advt,
        book_value=book_value,
        dps=dps,
        payout=payout,
        expected_growth=expected_growth,
        average_growth=average_growth,
        peg=peg,
        fair_price_graham=fair_price_graham,
        fair_price_bazin=fair_price_bazin,
        fair_price_gordon=fair_price_gordon,
        graham_valuation=graham_valuation,
        bazin_valuation=bazin_valuation,
        gordon_valuation=gordon_valuation,
    )

    return stock


def build_list_of_stocks(
    csv_info: list[str], headers: list[str], market_risk: float
):
    """
    Build a list of Stock from the info of a csv file
    """

    stocks = list()
    for line in csv_info:
        splited = line.split(';')
        try:
            stock = build_single_stock(splited, headers, market_risk)
        except (ValidationError, IndexError):
            continue
        stocks.append(stock)

    return stocks
