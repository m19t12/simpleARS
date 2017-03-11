import requests

"""
    utilities functions for the core functionality
"""

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.1'


def load_api_response(api_url):
    """
    method for loading an API Response using requests library
    :param api_url: the url for the endpoint you want to retrieve data
    :return: API response in json format
    """
    response = requests.get(api_url)
    return response.json()
