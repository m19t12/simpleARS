# coding=utf-8
import json
import os
from unittest import TestCase


class BaseARSTestCase(TestCase):
    """
    Basic class for initializing test data.
    """
    single_response_data = {}
    simple_response_data = {}
    list_response_data = []
    list_simple_response_data = []
    wrong_type_response = ""
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/"

    def setUp(self):
        """
        Loads the two json response for test usage.
        """
        with open(self.dir_path + 'single_response.json') as single_response:
            self.single_response_data = json.load(single_response)

        with open(self.dir_path + 'list_response.json') as list_response:
            self.list_response_data = json.load(list_response)

        with open(self.dir_path + 'simple_response.json') as simple_response_data:
            self.simple_response_data = json.load(simple_response_data)

        with open(self.dir_path + 'list_simple_response.json') as list_simple_response_data:
            self.list_simple_response_data = json.load(list_simple_response_data)
