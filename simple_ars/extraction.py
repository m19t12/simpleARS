# coding=utf-8
from simple_ars import search_object

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.6'

"""
extraction functionalities 
"""


def create_header(search_json):
    """
    method for creating header data for the csv file
    :param search_json: search parameters in json format
    :return: list of header data [header_1, header_2, header_3]
    """
    header = []
    search = search_object.SearchObject(search_json)
    select_keys = search.src_select

    for keys in select_keys:
        if isinstance(keys, dict):
            sub_header = create_header(keys)
            for sub_keys in sub_header:
                header.append(sub_keys)
        else:
            header.append(keys)

    return header


def ars_list(response_data, search_json):
    """
    method
    :param response_data:
    :param search_json:
    :return:
    """
    sub_data = {}
    search = search_object.SearchObject(search_json)
    _from = search.src_from
    _select = search.src_select
    sub_keys = False

    for select in _select:
        if isinstance(select, dict):
            sub_keys = True

    if sub_keys:
        if isinstance(response_data, dict):

            for key, value in response_data.items():
                if key == _from:
                    if isinstance(value, dict):
                        for select in _select:
                            sub_data = ars_list(value, select)
                    elif isinstance(value, list):
                        list_data = []
                        for element in value:
                            for select in _select:
                                sub_data = ars_list(element, select)
                            list_data.append(sub_data)
                        return list_data

        elif isinstance(response_data, list):
            list_data = []

            for items in response_data:
                sub_data = {}

                for select in _select:
                    if isinstance(select, dict):
                        sub_data.update(ars_list(items, select))
                    else:
                        sub_data[select] = items.get(select)
                list_data.append(sub_data)
            return list_data
    else:
        if isinstance(response_data, dict):
            if isinstance(response_data[_from], list):
                list_data = []

                for items in response_data[_from]:
                    sub_data = {}
                    for select in _select:
                        sub_data[select] = items.get(select)
                    list_data.append(sub_data)
                return list_data
            elif isinstance(response_data[_from], dict):
                for select in _select:
                    sub_data[select] = response_data[_from].get(select)
                return sub_data
        elif isinstance(response_data, list):
            list_data = []

            for items in response_data:
                for select in _select:
                    sub_data[select] = items.get(select)
            return list_data

    return sub_data
