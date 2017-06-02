# coding=utf-8
import json
import os
from unittest import TestCase


class BaseARSTestCase(TestCase):
    """
    Basic class for initializing test data.
    """
    single_response_data = {}
    list_response_data = []
    wrong_type_response = ""

    def setUp(self):
        """
        Loads the two json response for test usage.
        """
        with open('single_response.json') as single_response:
            self.single_response_data = json.load(single_response)

        with open('list_response.json') as list_response:
            self.list_response_data = json.load(list_response)

        self.service_api = 'https://services.tripinview.com/migration-services/hotels'
        self.cms_api = 'https://cms.tripinview.com/cms-api/v1/services/'
        self.credentials = {"username": os.environ['USERNAME'], "password": os.environ['PASSWORD']}
