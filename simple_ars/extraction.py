# coding=utf-8
from simple_ars import search_object

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.9'

"""
extraction functionalities 
"""


def ars_list(response_data, search_json):
    """
    method for extracted data in a list format.
    this method is ideal if you want to extract the retrieved data
    in csv format or to import them in data tables.
    :param response_data: the data you want to extract
    :param search_json: the search parameters in format {"from":["select]}
    :return: the extracted data in list format.
    """
    sub_data = {}

    sub_keys = False

    if isinstance(search_json, dict):
        search = search_object.SearchObject(search_json)
        _from = search.src_from
        _select = search.src_select

        for select in _select:
            if isinstance(select, dict):
                sub_keys = True
    else:
        _from = search_json
        _select = []

    if sub_keys:
        if isinstance(response_data, dict):
            list_data = []
            for key, value in response_data.items():
                if key == _from:
                    if isinstance(value, dict):
                        for select in _select:
                            data = ars_list(value, select)

                            if isinstance(data, list):
                                list_data = data
                            else:
                                list_data.append(data)

                        return list_data
                    elif isinstance(value, list):
                        list_data = []
                        for element in value:
                            sub_data = {}
                            for select in _select:
                                data = ars_list(element, select)

                                if isinstance(data, list):
                                    for i in data:
                                        sub_data.update(i)
                                else:
                                    sub_data.update(data)

                            list_data.append(sub_data)

                        return list_data
        elif isinstance(response_data, list):
            list_data = []

            for items in response_data:
                sub_data = {}

                for select in _select:
                    if isinstance(select, dict):
                        data = ars_list(items, select)
                        if data:
                            sub_data.update(*data)

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
                    list_data.append(
                        {
                            _from: sub_data
                        }
                    )
                return list_data

            elif isinstance(response_data[_from], dict):

                for select in _select:
                    sub_data[select] = response_data[_from].get(select)
                return {
                    _from: sub_data
                }

            else:
                sub_data[_from] = response_data.get(_from)
                return sub_data
        elif isinstance(response_data, list):
            list_data = []

            for items in response_data:
                sub_data = {}
                for select in _select:
                    sub_data[select] = items.get(select)
                list_data.append(sub_data)
            return list_data
