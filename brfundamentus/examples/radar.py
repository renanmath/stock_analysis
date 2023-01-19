import json
from copy import copy

from brfundamentus.models.stock_market import StockMarket

"""
This script is an example of how to use some of the functionalities to run a radar of good stocks
"""


def print_list(list_of_stocks: list):
    for stock in list_of_stocks:
        stock.print_valuations()

    print('-' * 50)


def union_lists(list1: list, list2: list) -> list:
    union = copy(list1)
    union += [x for x in list2 if x not in list1]

    return union

def radar(path_to_csv: str, path_to_parameters:str):
    # First, instantiate a StockMarket object
    # This class is responsible to perform the valuations
    # and has some useful filter methods
    market = StockMarket.read_from_csv(path_to_csv)

    # Then, define your own filters
    # They have to be dictionaries of three keys:
    # parameter, cut_criterion and reverse_cut.
    # See the docstring of method get_top_stocks_by_conditions
    # In this example, we will pull the parameters from a json file
    # named radar_parameters.json
    # In the repository we include a radar_parameters_example.json
    # Copy this file and change its name to radar_parameters.json
    # then set your own personal parameters


    with open(path_to_parameters) as file:
        parameters = json.load(file)

    filtros_comuns = parameters['common']

    filtros = parameters['first']

    filtros += filtros_comuns

    rank = {'parameter': 'graham_valuation', 'ascending': False}

    initial_list = market.get_top_stocks_by_list_of_conditions(
        conditions=filtros, sort_by=rank, num_stocks=600
    )

    print('\nPrimeira lista')
    print_list(initial_list)
    print(len(initial_list))

    # second list

    filtros = parameters['second']

    filtros += filtros_comuns

    second_list = union_lists(
        initial_list,
        market.get_top_stocks_by_list_of_conditions(
            conditions=filtros, sort_by=rank, num_stocks=600
        ),
    )

    print('\nSegunda lista')
    print_list(second_list)
    print(len(second_list))

    filtros = parameters['third']

    filtros += filtros_comuns

    third_list = union_lists(
        second_list,
        market.get_top_stocks_by_list_of_conditions(
            conditions=filtros, sort_by=rank, num_stocks=600
        ),
    )

    print('\nTerceira lista')
    print_list(third_list)
    print(len(third_list))


if __name__ == '__main__':
    radar('statusinvest-busca-avancada.csv', 'brfundamentus/examples/radar_parameters.json')
