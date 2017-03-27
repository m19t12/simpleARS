import os
import unittest

from simpleARS import core_utils


class CoreUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.api_url_from_services = "https://services.tripinview.com/migration-services/hotels"
        self.api_url_from_ads = "https://business.tripinview.com/public" \
                                "/ads.json?$filter=zone/scope%20eq%20%27subscription%27&$top=-1"
        self.secure_api_url = "https://business.tripinview.com/login.html?returnUrl=%2Fad%2Findex.json" \
                              "%3F%2524filter%3Dzone%2520eq%25207%2520or%2520zone%2520eq%25203and%2520" \
                              "status%2520eq%25206%26%2524select%3Did%252Cname%26%2524top%3D-1"

    def test_if_load_json_response_from_api_returns_json(self):
        api_response = core_utils.load_api_response(self.api_url_from_services)
        self.assertIsInstance(api_response, dict)

    def test_if_load_json_response_from_api_returns_list(self):
        api_response = core_utils.load_api_response(self.api_url_from_ads)
        self.assertIsInstance(api_response, list)

    def test_if_load_json_response_from_secure_api(self):
        credentials = {"username": os.environ['USERNAME'], "password": os.environ['PASSWORD']}
        api_response = core_utils.load_api_response(self.api_url_from_ads, credentials)
        self.assertIsInstance(api_response, list)
