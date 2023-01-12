from typing import Optional
from pydantic import PositiveInt, PositiveFloat
from pydantic.dataclasses import dataclass
from brfundamentus.utils.utils import round_value as rv


@dataclass
class Stock:
    """
    Class to model a brazilian stock
    It contains information about indicators
    """

    ticker: str
    price: PositiveFloat
    dy: Optional[float]  # dividend yield
    roe: float  # return on equity
    roic: Optional[float]  # return on invested capital
    roa: Optional[float]  # return on assets
    eps: Optional[float]  # earnings per share (LPA, lucro por ação, in BR)
    # (in BR, preço sobre valor patrimonial, P/VP)
    price_to_book: Optional[float]
    gross_margin: Optional[float]  # margem bruta
    net_margin: Optional[float]  # margem líquida
    ebit_margin: Optional[float]  # margem ebit
    current_liquidity: Optional[float]  # liquidez corrente
    # book value per share (in BR, valor patrimonial por ação, VPA)
    bvps: Optional[float]
    price_per_profit: float  # preço por lucro, PL
    ev_per_ebit: Optional[float]  # EV/EBIT
    cagr: Optional[float] = None  # compound annual growth rate
    adtv: Optional[float] = None  # averenge daily trading volume
    book_value: Optional[float] = None  # valor de mercado
    # dívida líquida sobre patrimônio
    net_debt_to_equity: Optional[float] = None
    greenblatt_rank: Optional[PositiveInt] = None
    # dividend per share (in Br, DPA - dividendo por ação)
    dps: Optional[float] = None
    payout: Optional[float] = None
    expected_growth: Optional[float] = None
    average_growth: Optional[float] = None
    peg: Optional[float] = None
    fair_price_graham: Optional[float] = None
    fair_price_bazin: Optional[float] = None
    fair_price_gordon: Optional[float] = None
    graham_valuation: Optional[float] = None
    bazin_valuation: Optional[float] = None
    gordon_valuation: Optional[float] = None

    def print_valuations(self):
        print(
            f'{self.ticker}: {self.price} | {rv(self.greenblatt_rank)} | {rv(self.graham_valuation)} | {rv(self.bazin_valuation)} | {rv(self.gordon_valuation)} | {rv(self.average_growth)} | {rv(self.dy)}'
        )

    def __repr__(self) -> str:
        return f'{self.ticker} ({self.price})'
