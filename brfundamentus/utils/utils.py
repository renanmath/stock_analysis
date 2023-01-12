"""
Utils methods
"""


def parse_str_to_float(x: str, d: float = 1):
    try:
        return float(x.strip(' "\n\t').replace(',', '.')) / d
    except ValueError:
        return None


def round_value(x, r=4):
    try:
        return round(x, r)
    except TypeError:
        return x


def compute_greenblatt_rank(stocks):
    """
    Computes the greenblatt rank of every stock
    """
    ranks_dict = {
        stock.ticker: {
            'rank_ev_ebit': None,
            'rank_roic': None,
            'total_rank': None,
        }
        for stock in stocks
    }

    stocks_with_positive_ev_ebit = [
        stock
        for stock in stocks
        if stock.ev_per_ebit is not None and stock.ev_per_ebit > 0
    ]
    stocks_with_positive_ev_ebit.sort(key=lambda st: st.ev_per_ebit)
    for idx, stock in enumerate(stocks_with_positive_ev_ebit):
        ranks_dict[stock.ticker]['rank_ev_ebit'] = idx + 1

    stocks_with_positive_roic = [
        stock for stock in stocks if stock.roic is not None and stock.roic > 0
    ]
    stocks_with_positive_roic.sort(key=lambda st: st.roic, reverse=True)
    for idx, stock in enumerate(stocks_with_positive_roic):
        ranks_dict[stock.ticker]['rank_roic'] = idx + 1

    for stock in stocks:
        rank_ev_ebit = ranks_dict[stock.ticker]['rank_ev_ebit']
        rank_roic = ranks_dict[stock.ticker]['rank_roic']
        if rank_ev_ebit is not None and rank_roic is not None:
            ranks_dict[stock.ticker]['total_rank'] = rank_ev_ebit + rank_roic

    stocks_with_greenblatt_rank = [
        stock
        for stock in stocks
        if ranks_dict[stock.ticker]['total_rank'] is not None
    ]
    stocks_with_greenblatt_rank.sort(
        key=lambda st: ranks_dict[st.ticker]['total_rank']
    )

    for idx, stock in enumerate(stocks_with_greenblatt_rank):
        stock.greenblatt_rank = idx + 1
