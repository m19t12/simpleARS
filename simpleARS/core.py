import requests


def load_api_response(api_url):
    response = requests.get(api_url)
    return response.json()


def list_response_generator(list_response):
    for data in list_response:
        yield data


def api_response_type(response_object):
    if isinstance(response_object, dict):
        return response_object
    elif isinstance(response_object, list):
        return list_response_generator(response_object)
    else:
        raise TypeError("Api response must be a list or a dict not a {}".format(type(response_object)))
