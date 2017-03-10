import requests


def load_api_response(api_url):
    response = requests.get(api_url)
    return response.json()
