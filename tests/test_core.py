import unittest

from simpleARS import core


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.retrieved_data = {'key_1': 'value_1', 'key_2': 'value_2', 'key_list_1': ['list_value_1', 'list_value_2', {
            'sub_key1': ["sub_data_1", "sub_data_2"]}]}
        self.retrieved_single_data = 'value_1'
        self.retrieved_sub_data = {'key_list_1': ['list_value_1', 'list_value_2', {
            'sub_key1': ["sub_data_1", "sub_data_2"]}]}
        self.from_key = "key_1"
        self.select_keys = ['key_1', 'key_2']
        self.select_unknown_keys = ['key_error_1', 'key_error_2']
        self.select_list_key = {"key_list_1": ['list_value_1', 'list_value_2']}
        self.select_single_object = []
        self.select_sub_data = {'key_list_1': ['sub_key1']}

    def test_if_search_and_retrieve_returns_correct_data(self):
        result = core.search_and_retrieve(self.retrieved_data, self.select_keys, self.from_key)
        self.assertEqual(result, {'key_1': 'value_1', 'key_2': 'value_2'})

    def test_if_search_and_retrieve_returns_none(self):
        result = core.search_and_retrieve(self.retrieved_data, self.select_unknown_keys, self.from_key)
        self.assertEqual(result, None)

    def test_if_search_and_retrieve_returns_key_with_list_value(self):
        result = core.search_and_retrieve(self.retrieved_data, self.select_list_key, self.from_key)
        self.assertEqual(result, {'key_list_1': ['list_value_1', 'list_value_2', {
            'sub_key1': ["sub_data_1", "sub_data_2"]}]})

    def test_if_search_and_retrieve_returns_single_object(self):
        result = core.search_and_retrieve(self.retrieved_single_data, self.select_single_object, self.from_key)
        self.assertEqual(result, {'key_1': 'value_1'})

    def test_if_search_and_retrieve_returns_sub_data(self):
        result = core.search_and_retrieve(self.retrieved_sub_data, self.select_sub_data, self.from_key)
        self.assertEqual(result, {'key_list_1': ['list_value_1', 'list_value_2', {
            'sub_key1': ["sub_data_1", "sub_data_2"]}]})
