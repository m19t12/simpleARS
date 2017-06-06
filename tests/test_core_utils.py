# coding=utf-8
from simple_ars import core_utils
from tests import BaseARSTestCase


class CoreUtilsTestCase(BaseARSTestCase):
    def setUp(self):
        super(CoreUtilsTestCase, self).setUp()
        self.api_url_from_services = "https://services.tripinview.com/migration-services/hotels"
        self.api_url_from_ads = "https://business.tripinview.com/public" \
                                "/ads.json?$filter=zone/scope%20eq%20%27subscription%27&$top=-1"
        self.secure_api_url = "https://cms.tripinview.com/cms-api/v1/services/"

    def test_if_load_json_response_from_api_returns_json(self):
        api_response = core_utils.load_api_response(self.api_url_from_services)
        self.assertIsInstance(api_response, dict)

    def test_if_load_json_response_from_api_returns_list(self):
        api_response = core_utils.load_api_response(self.api_url_from_ads)
        self.assertIsInstance(api_response, list)

    def test_if_load_json_response_from_secure_api(self):
        api_response = core_utils.load_api_response(self.secure_api_url, self.credentials)
        self.assertIsInstance(api_response, list)
