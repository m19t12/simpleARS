import os
import unittest

from simple_ars import core, search_object


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
        self.search_ads = {"~": ["id", "name", "index"]}

        self.services_end_point = "https://services.tripinview.com/migration-services/hotels"
        self.ads_end_point = "https://business.tripinview.com/" \
                             "public/ads.json?$filter=zone/scope%20eq%20%27subscription%27&$top=-1"

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

    def test_if_retrieve_data_method_returns_correct_results(self):
        results = core.retrieve_data(self.services_end_point, self.search)
        self.assertIsInstance(results, dict)

    def test_if_retrieve_data_method_returns_correct_csv_file(self):
        core.retrieve_data(self.services_end_point, self.search, mode="csv", csv_file_name="tests/test_output")
        csv_file = ""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        for file in os.listdir(dir_path):
            if file.endswith(".csv"):
                csv_file = file
        self.assertEqual(csv_file, "test_output.csv")
        os.remove("tests/" + csv_file)

    def test_if_retrieve_data_method_returns_list_instance(self):
        results = core.retrieve_data(self.ads_end_point, self.search_ads)
        self.assertIsInstance(results, list)

    def test_if_retrieve_data_returns_default_extraction_mode(self):
        core.retrieve_data(self.ads_end_point, self.search_ads, None, "random_mode")

    def test_if_ars_returns_correct_data(self):
        results = core.ars(self.data, self.search_root)
        self.assertEqual(results, {"from_data_1": "data_1", "from_data_2": "data_2", "from_data_3": "data_3"})

    def test_if_ars_raises_type_error_if_retrieved_data_is_wrong_type(self):
        with self.assertRaises(TypeError):
            core.ars("data", self.search_root)
