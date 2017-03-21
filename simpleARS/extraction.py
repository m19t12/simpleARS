import csv
import logging


def create_header(retrieved_data):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    header = []

    for key in retrieved_data:
        header.append(key)

    if len(header) > 1:
        sub_headers = []
        for key in header:
            if isinstance(retrieved_data[key], dict):
                for dict_key in list(retrieved_data[key]):
                    sub_headers.append(dict_key)
            elif isinstance(retrieved_data[key], list):
                logger.info("Relationship one to many limit one activate")
                list_data = retrieved_data[key][0]
                list_header = create_header(list_data)
                for list_keys in list_header:
                    sub_headers.append(list_keys)
            else:
                sub_headers.append(key)
        return sub_headers
    else:
        key = header[0]
        if isinstance(retrieved_data[key], list):
            data = retrieved_data[key][0]
            header = create_header(data)
        return header


def find_relationships(save_data):
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
                list_item = get_save_data(retrieved_data[key])
                for data in list_item:
                    dict_object[key] = data
            else:
                dict_object[key] = retrieved_data[key]
        list_data.append(dict_object)
        return list_data
    else:
        key = headers[0]
        if isinstance(retrieved_data[key], list):
            processed = find_relationships(retrieved_data[key])
            return processed


def csv_extraction(retrieved_data):
    header = create_header(retrieved_data)
    save_data = get_save_data(retrieved_data)

    with open('names.csv', 'w') as csv_file:
        fieldnames = header
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in save_data:
            writer.writerow(data)
