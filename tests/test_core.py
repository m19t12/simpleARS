import unittest

from simpleARS import core


class CoreTestCase(unittest.TestCase):
    def setUp(self):
        self.api_response = {'data':
            {'records': [
                {'dataset_id': 1000, 'amentities': [{'name': 'bar', 'id': 1}],
                 'weather': {'wind_speed': 'full'}}
            ]}, 'total': 300}
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
