# -*- coding: utf-8 -*-
from collections import OrderedDict
from datetime import date, timedelta
from decimal import Decimal

from get_name import *
from read_data import get_chunk_data_by_name_and_date


def calculate_profit(data):
    return round(((data[-1] - data[0]) / data[0]) * 100, 2)


def calculate_most_loss(data):
    min_val = min(data)
    # print(data[0], type(data[0]), min_val, type(min_val))
    ret = round(((data[0] - min_val) / min_val) * 100, 2)
    if ret == 0:
        print(data[0], min_val[0])
    return ret


def get_stock_name_of_growth_more_than_percent_with_period(stock_type, growth: Decimal, lose: Decimal, periods):
    """
    get Stock Name that have growth more than growth(unit = %) in period(unit = day).
    :param growth: (type: decimal)
    :param lose: (type: decimal)
    :param periods: (type: int)
    :param stock_type : stock type
    :return: stock_name, growth,
    """
    print(stock_type, growth, lose, periods)
    yesterday = date.today() - timedelta(1)
    if stock_type == 'SET&MAI':
        stock_names = get_stock_name_list_exw()
    elif stock_type == 'SET100':
        stock_names = get_stock_name_list_of_set100()
    elif stock_type == 'MAI':
        stock_names = get_stock_name_list_of_mai()
    elif stock_type == 'WARRANT':
        stock_names = get_stock_name_list_of_warrant()
    elif stock_type == 'ALL':
        stock_names = get_stock_active_name_list()
    else:
        stock_names = get_stock_active_name_list()

    # stock_names = ['AOT']
    ret_json = []
    dictionary = OrderedDict()
    template_name = 'stock growth more than ' + str(int(growth)) + ' in ' + str(int(periods)) + ' day'
    dictionary['template_name'] = template_name
    dictionary['stock_name'] = []
    dictionary['growth'] = []
    cp = None
    most_lose = None
    for s in stock_names:
        # stock_data = get_chunk_data_by_name_and_date(s, 'day', yesterday.strftime("%m/%d/%Y"), periods)[1]
        stock_data = get_chunk_data_by_name_and_date(s, 'day', 0, periods)[1]
        # print(stock_data)
        # stock_data = get_chunk_data_by_name_and_date(s, '12/16/2016', periods)[1]
        try:
            cp = calculate_profit(stock_data)
            most_lose = calculate_most_loss(stock_data)
        except TypeError:
            pass
            # print("can't calculate for'" + s)
        if cp is not None and most_lose is not None:
            if cp > growth and most_lose < lose:
                dictionary['stock_name'] = s
                dictionary['growth'] = cp
                dictionary['most_lose'] = most_lose
                # print(s, cp, most_lose)
                # ret_json.append(json.dumps(dictionary, ensure_ascii=False))
                ret_json.append(s)
    message = dict()
    msg = str(ret_json)[1:-1]
    msg = msg.replace("'", "")
    msg = msg.replace(",", "")
    message['messages'] = [{"text": u"SCAN RESULT \n " + msg}]
    if len(ret_json) == 0:
        message['messages'] = [{"text": u"SCAN RESULT = 0\n " + msg}]
    return message


def get_growth_stock(stock_type, growth: Decimal, lose: Decimal, periods):
    """
    get Stock Name that have growth more than growth(unit = %) in period(unit = day).
    :param growth: (type: decimal)
    :param lose: (type: decimal)
    :param periods: (type: int)
    :param stock_type : stock type
    :return: stock_name, growth,
    """

    yesterday = date.today() - timedelta(1)
    if stock_type == 'SET&MAI':
        stock_names = get_stock_name_list_exw()
    elif stock_type == 'SET100':
        stock_names = get_stock_name_list_of_set100()
    elif stock_type == 'MAI':
        stock_names = get_stock_name_list_of_mai()
    elif stock_type == 'WARRANT':
        stock_names = get_stock_name_list_of_warrant()
    else:
        stock_names = get_stock_active_name_list()

    # stock_names = ['AOT']
    ret_json = []
    dictionary = OrderedDict()
    template_name = 'stock growth more than ' + str(int(growth)) + ' in ' + str(int(periods)) + ' day'
    dictionary['stock_name'] = []
    dictionary['data'] = []
    dictionary['retval'] = []
    cp = None
    most_lose = None
    for s in stock_names:
        # stock_data = get_chunk_data_by_name_and_date(s, 'day', yesterday.strftime("%m/%d/%Y"), periods)[1]
        stock_data = get_chunk_data_by_name_and_date(s, 'day', 0, periods)
        # print(stock_data)
        # stock_data = get_chunk_data_by_name_and_date(s, '12/16/2016', periods)[1]
        try:
            cp = calculate_profit(stock_data[1])
            most_lose = calculate_most_loss(stock_data[1])
        except TypeError:
            pass
            # print("can't calculate for'" + s)
        if cp is not None and most_lose is not None:
            if cp > growth and most_lose < lose:
                dictionary['stock_name'].append(s)
                dictionary['data'].append(stock_data)
                dictionary['retval'].append(1)
            else:
                if len(dictionary['retval']) > 1:
                    if dictionary['retval'][-1] == 1 and stock_data is not None:
                        dictionary['stock_name'].append(s)
                        dictionary['data'].append(stock_data)
                        dictionary['retval'].append(0)
    return dictionary


def get_feature(stock_type, periods):
    if stock_type == 'SET&MAI':
        stock_names = get_stock_name_list_exw()
    elif stock_type == 'SET100':
        stock_names = get_stock_name_list_of_set100()
    elif stock_type == 'MAI':
        stock_names = get_stock_name_list_of_mai()
    elif stock_type == 'WARRANT':
        stock_names = get_stock_name_list_of_warrant()
    else:
        stock_names = get_stock_active_name_list()

    dictionary = OrderedDict()
    dictionary['stock_name'] = []
    dictionary['data'] = []

    for s in stock_names:
        stock_data = get_chunk_data_by_name_and_date(s, 'day', 0, periods)
        dictionary['stock_name'].append(s)
        dictionary['data'].append(stock_data)

    return dictionary


# print(get_stock_name_of_growth_more_than_percent_with_period(stock_type='SET100', growth=Decimal(5), lose=Decimal(100), periods=30))
# print(get_stock_name_of_growth_more_than_percent_with_period(stock_type='MAI', growth=Decimal(100), lose=Decimal(5), periods=30))
# print(get_stock_name_of_growth_more_than_percent_with_period(stock_type='SET&MAI', growth=Decimal(100), lose=Decimal(5), periods=30))
# print(get_stock_name_of_growth_more_than_percent_with_period(stock_type='WARRANT', growth=Decimal(100), lose=Decimal(5), periods=30))
# print(get_stock_name_of_growth_more_than_percent_with_period('SET100', Decimal(0), Decimal(100), 2))
# print(get_stock_name_of_growth_more_than_percent_with_period('SET&MAI', Decimal(0), Decimal(100), 5))

# message = get_stock_name_of_growth_more_than_percent_with_period('SET&MAI', Decimal(0), Decimal(100), 2)
# print(message)
# message = get_stock_name_of_growth_more_than_percent_with_period('SET&MAI', Decimal(0), Decimal(100), 5)
# print(message)
# message = get_stock_name_of_growth_more_than_percent_with_period('SET&MAI', Decimal(0), Decimal(100), 20)
# print(message)