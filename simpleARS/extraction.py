import csv

from simpleARS import search_object

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.4'

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


def find_relationships(save_data):
    """
    method for finding if data relationship is one to many [data_1, [list_data_2], data_2]
    :param save_data: retrieved data from the filtering process
    :return: return the data with the relationship
    """
    processed_data = {}
    list_data = []

    for data in save_data:
        for key, value in data.items():
            if isinstance(data[key], list):
                limit_item = data[key][0]
                for sub_data in limit_item:
                    processed_data[sub_data] = limit_item[sub_data]
            elif isinstance(data[key], dict):
                for dict_key, dict_value in data[key].items():
                    processed_data[dict_key] = dict_value
            else:
                processed_data[key] = data[key]
        list_data.append(processed_data)

    return list_data


def get_save_data(retrieved_data):
    """
    method for serializing the retrieved data and converted for csv extraction
    :param retrieved_data: the data retrieved from the core retrieve process 
    :return: return the data for saving in array containing dicts [{dict_1}, {dict_2}]
    """
    headers = []

    for key in retrieved_data:
        headers.append(key)

    if len(headers) > 1:
        list_data = []
        dict_object = {}
        for key in headers:
            if isinstance(retrieved_data[key], list):
                list_item = retrieved_data[key][0]
                for data in list_item:
                    dict_object[data] = list_item[data]
            elif isinstance(retrieved_data[key], dict):
                dict_object[key] = retrieved_data[key]
            else:
                dict_object[key] = retrieved_data[key]
        list_data.append(dict_object)
        return list_data
    else:
        key = headers[0]
        if isinstance(retrieved_data[key], list):
            processed = find_relationships(retrieved_data[key])
            return processed


def csv_extraction(retrieved_data, search_data, csv_file_name):
    """
    the main extraction method for creating csv file
    :param retrieved_data: the data retrieved from the core functionality
    :param search_data: the search parameters in json format
    :param csv_file_name: the name for the csv file you created
    :return: the csv file
    """
    header = create_header(search_data)
    save_data = get_save_data(retrieved_data)

    with open(csv_file_name + '.csv', 'w') as csv_file:
        fieldnames = header
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in save_data:
            writer.writerow(data)
