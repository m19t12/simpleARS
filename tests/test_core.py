import unittest

from simpleARS import core, search_object


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.api_response = {'data':
            {'records': [
                {'dataset_id': 1000, 'amentities': [{'name': 'bar', 'id': 1}],
                 'weather': {'wind_speed': 'full'}}
            ]}, 'total': 300}
        self.data = {"from_data_1": "data_1", "from_data_2": "data_2", "from_data_3": "data_3"}
        self.search_root = {"~": ["from_data_1", "from_data_2", "from_data_3"]}
        self.search = {'data': [{'records': ['dataset_id', {'amentities': ['name', 'id']}]}]}
        self.retrieved_records = {'dataset_id': 1000, 'amentities': [{'name': 'bar', 'id': 1}],
                                  'weather': {'wind_speed': 'full'}}
        self.select_records = ['dataset_id', {'amentities': ['name', 'id']}, {'weather': ['wind_speed']}]
        self.select_records_no_key = ['dataset_id', {'amentities': ['name', 'id']}, {'weather': ['wind_speed']},
                                      'no_key']
        self.select_records_no_from_key = ['dataset_id', {'no_from_key': ['name', 'id']}, {'weather': ['wind_speed']},
                                      'no_key']

    def test_if_search_and_retrieve_return_records(self):
        results = core.search_and_retrieve(self.retrieved_records, self.select_records)
        self.assertEqual(results, {'dataset_id': 1000, 'amentities': [{'name': 'bar', 'id': 1}],
                                   'weather': {'wind_speed': 'full'}})

    def test_if_one_key_doesnt_exist(self):
        results = core.search_and_retrieve(self.retrieved_records, self.select_records_no_key)
        self.assertEqual(results, {'dataset_id': 1000, 'amentities': [{'name': 'bar', 'id': 1}],
                                   'weather': {'wind_speed': 'full'}, 'no_key': None})

    def test_if_search_and_retrieve_return_top_data(self):
        results = core.search_and_retrieve(self.api_response['total'], [], 'total')
        self.assertEqual(results, {'total': 300})

    def test_if_retrieve_sub_data_returns_correct_data_when_tilda_sign_used(self):
        search_obj = search_object.SearchObject(self.search_root)
        results = core.retrieve_sub_data(self.data, search_obj)
        self.assertEqual(results, {"from_data_1": "data_1", "from_data_2": "data_2", "from_data_3": "data_3"})

    def test_if_retrieve_sub_data_returns_none_when_no_key_exists(self):
        search_obj = search_object.SearchObject({"data": ["data_1", "data_2"]})
        results = core.retrieve_sub_data(self.data, search_obj)
        self.assertEqual(results, None)
