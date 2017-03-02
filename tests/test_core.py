import unittest

from simpleARS import core


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.api_url_from_services = "https://services.tripinview.com/migration-services/hotels"
        self.api_url_from_ads = "https://business.tripinview.com/public/ads.json?$filter=zone/scope%20eq%20%27subscription%27&$top=-1"

    def test_if_load_json_response_from_api_returns_json(self):
        api_response = core.load_api_response(self.api_url_from_services)
        self.assertIsInstance(api_response, dict)

    def test_if_load_json_response_from_api_returns_list(self):
        api_response = core.load_api_response(self.api_url_from_ads)
        self.assertIsInstance(api_response, list)

    def test_if_type_json_api_response_returns_json_object(self):
        api_response = core.load_api_response(self.api_url_from_services)
        data = core.api_response_type(api_response)
        self.assertIsInstance(data, dict)

    def test_if_type_list_api_response_returns_generator_object(self):
        api_response = core.load_api_response(self.api_url_from_ads)
        data = core.api_response_type(api_response)
        self.assertIsInstance(data, object)

    def test_if_api_response_type_raises_error_when_wrong_type_passed(self):
        with self.assertRaises(TypeError):
            data = core.api_response_type(1234)
