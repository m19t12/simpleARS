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


def csv_extraction(retrieved_data):
    header = create_header(retrieved_data)
