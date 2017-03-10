import logging

from simpleARS import core_utils, search_object


def search_and_retrieve(data, select_keys, from_key):
    dict_item = {}
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
                    dict_item = None
    else:
        dict_item[from_key] = data
    return dict_item


def retrieve_sub_data(sub_data, search):
    from_key = search.src_from
    select_keys = search.src_select

    if from_key in sub_data:
        items = search_and_retrieve(sub_data[from_key], select_keys, from_key)
    else:
        items = None
    return items


def retrieve_list_data(list_data, search):
    from_key = search.src_from
    select_keys = search.src_select
    items = []

    for data in list_data:
        items.append(search_and_retrieve(data, select_keys, from_key))
    return items


def retrieve_data(api_url, search, mode):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    api_response = core_utils.load_api_response(api_url)
    search = search_object.SearchObject(search)

    if isinstance(api_response, dict):
        retrieved_data = retrieve_sub_data(api_response, search)
    elif isinstance(api_response, list):
        retrieved_data = retrieve_list_data(api_response, search)
    else:
        raise TypeError("Wrong Type Response!!! Response must be list or dict not {}".format(type(api_response)))

    if mode == "csv":
        logger.info("CSV")
    else:
        logger.warning("Unknown mode.Enabling default mode csv")
        logger.info("CSV")
