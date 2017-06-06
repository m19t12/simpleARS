# coding=utf-8
import csv

from simple_ars import search_object

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.5'

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


def retrieve_data(data, header):
    """
    method for processing the retrieved data and find the correct relationship to display in csv format.
    :param data: data to be processed.
    :param header: the header we want to extract.
    :return: return the data corresponding to the header.
    """
    dict_data = {}

    if isinstance(data, dict):
        if header in data.keys():
            dict_data.update({header: data[header]})
        else:
            for key, value in data.items():
                if isinstance(value, list):
                    if value:
                        list_data = retrieve_data(value[0], header)
                        dict_data.update(list_data)
                    else:
                        dict_data.update({header: value})
                elif isinstance(value, dict):
                    sub_data = retrieve_data(value, header)
                    dict_data.update(sub_data)
    elif isinstance(data, list):
        dict_data.update(retrieve_data(data[0], header))
    return dict_data


def get_save_data(retrieved_data, headers):
    """
    method for serializing the retrieved data and converted for csv extraction
    :param headers: the headers for the csv columns
    :param retrieved_data: the data retrieved from the core retrieve process
    :return: return the data for saving in array containing dicts [{dict_1}, {dict_2}]
    """

    csv_data = []

    if isinstance(retrieved_data, dict):
        dict_data = {}
        for header in headers:
            data = retrieve_data(retrieved_data, header)
            dict_data.update(data)
        csv_data.append(dict_data)
    elif isinstance(retrieved_data, list):
        item = []
        for data in retrieved_data:
            dict_data = {}
            for header in headers:
                dict_data.update(retrieve_data(data, header))
            item.append(dict_data)
        csv_data = item
    return csv_data


def csv_extraction(retrieved_data, search_data, csv_file_name):
    """
    the main extraction method for creating csv file
    :param retrieved_data: the data retrieved from the core functionality
    :param search_data: the search parameters in json format
    :param csv_file_name: the name for the csv file you created
    :return: the csv file
    """
    headers = create_header(search_data)
    save_data = get_save_data(retrieved_data, headers)

    with open(csv_file_name + '.csv', 'w') as csv_file:
        fieldnames = headers
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in save_data:
            writer.writerow(data)

    return save_data
