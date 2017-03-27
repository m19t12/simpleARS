import requests

"""
    utilities functions for the core functionality
"""

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.2'


def load_api_response(api_url, credentials=None):
    """
    method for loading an API Response using requests library
    :param api_url: the url for the endpoint you want to retrieve data
    :param credentials: credentials for using secure endpoints
    :return: API response in json format
    """

    if credentials is not None:
        username = credentials['username']
        password = credentials['password']

        response = requests.get(api_url, auth=(username, password))
    else:
        response = requests.get(api_url)

    return response.json()
