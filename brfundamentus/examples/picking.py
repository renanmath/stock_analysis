import json
from brfundamentus.models.stock_market import StockMarket
from brfundamentus.utils.utils import print_list_of_stocks


def stock_picking(path_to_parameters: str, path_to_csv: str):

    market = StockMarket.read_from_csv(path_to_csv)

    with open(path_to_parameters) as file:
        parameters = json.load(file)

    base_params = parameters['base']
    sort_dict = {'parameter': 'graham_valuation', 'ascending': False}

    for param_list in parameters['lists']:
        name = param_list['name']
        my_params = base_params + param_list['filters']

        stocks_picked = market.get_top_stocks_by_list_of_conditions(
            conditions=my_params, sort_by=sort_dict
        )

        print(f'\n\n*** {name.upper()} ***\n')
        print_list_of_stocks(stocks_picked)


if __name__ == '__main__':
    stock_picking(
        'brfundamentus/examples/picking_parameters.json',
        'statusinvest-busca-avancada.csv',
    )
