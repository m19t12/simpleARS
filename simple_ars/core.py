# coding=utf-8
from simple_ars import search_object

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.7'

"""
simpleARS core functionality for retrieving data
"""


def search_and_retrieve(data, select_keys, from_key=""):
    """
    method for searching and retrieving data.
    :param data: the data from wich you want to retrieve
    :param select_keys: a list with keys
    :param from_key: the from_key is mostly used when we want to retrieve top level objects
    :return: return a dictionary item with the data we want to get
    """
    dict_item = {}
    if data:
        if len(select_keys) != 0:
            for key in select_keys:
                if isinstance(key, dict):
                    search = search_object.SearchObject(key)
                    if isinstance(data[search.src_from], list):
                        dict_item[search.src_from] = retrieve_list_data(data[search.src_from], search)
                    else:
                        dict_item[search.src_from] = retrieve_sub_data(data, search)
                else:
                    if key in data:
                        dict_item[key] = data[key]
                    else:
                        dict_item[key] = None
        else:
            dict_item[from_key] = data
    return dict_item


def retrieve_sub_data(sub_data, search):
    """
    method to use when we want to retrieve dictionary data.
    :param sub_data: dictionary data
    :param search: search object
    :return: return the sub data
    """
    from_key = search.src_from
    select_keys = search.src_select

    if from_key in sub_data:
        items = search_and_retrieve(sub_data[from_key], select_keys, from_key)
    elif from_key == "~":
        items = search_and_retrieve(sub_data, select_keys, from_key)
    else:
        items = None
    return items


def retrieve_list_data(list_data, search):
    """
    method for retrieving list data.
    :param list_data: list of dictionary data
    :param search: search object
    :return: list of retrieved data in dictionary format
    """

    from_key = search.src_from
    select_keys = search.src_select
    items = []

    for data in list_data:
        items.append(search_and_retrieve(data, select_keys, from_key))
    return items


def ars(api_response, search):
    """
    basic method for searching and retrieving data in dictionary format.
    :param api_response: data returned by your endpoint
    :param search: search object in dictionary format
    :return: the extracted data
    """
    search_obj = search_object.SearchObject(search)

    if isinstance(api_response, dict):
        retrieved_data = retrieve_sub_data(api_response, search_obj)
    elif isinstance(api_response, list):
        retrieved_data = retrieve_list_data(api_response, search_obj)
    else:
        raise TypeError("Wrong Type Response!!! Response must be list or dict not {}".format(type(api_response)))
    return retrieved_data
