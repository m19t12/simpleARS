# coding=utf-8
import os
import unittest

from simple_ars import extraction


class TestExtraction(unittest.TestCase):
    def setUp(self):
        self.search = {
            "data": [{"records": ["dataset_id", "category", {"amentities": ["name", "id"]},
                                  {"weather": ["airport_ref", "wind_speed"]}]}]}

        self.search_v2 = {"data": [{"records": [{"amentities": ["name", "id"]}]}]}

        self.search_v3 = {"data": ["total", {"records": ["dataset_id"]}]}

        self.search_v4 = {"~": [{"data": ["total", {"records": ["dataset_id"]}]}, "status_text", "status_code"]}

        self.search_v5 = {"~": ["data", "status_text", "status_code"]}

        self.search_v6 = {"~": ["id", "name", {"profile": ["name", "email"]}, {"facet": ["name", "dateCreated"]}]}

        self.retrieved_data = {"from_data_1": "data_1", "from_data_2": "data_2",
                               "from_list_data_1": [{"from_sub_data_1": "data_1"}, {"from_sub_data_2": "data_2"}]}

        self.retrieved_data_v2 = {
            "from_data_1": [{"from_sub_data_1": [{"from_list_data_1": "data_1"}, {"from_list_data_2": "data_2"}]}]}

        self.search_retrieve_data = {
            "~": ["from_data_1", "from_data_2", {"from_list_data_1": ["from_sub_data_1", "from_sub_data_2"]}]}

    def test_check_if_create_header_function_returns_correct_header(self):
        header = extraction.create_header(self.search)
        self.assertEqual(header, ["dataset_id", "category", "name", "id", "airport_ref", "wind_speed"])

    def test_check_if_create_header_function_returns_correct_header_v2(self):
        header_v2 = extraction.create_header(self.search_v2)
        self.assertEqual(header_v2, ["name", "id"])

    def test_check_if_create_header_function_returns_correct_header_v3(self):
        header_v3 = extraction.create_header(self.search_v3)
        self.assertEqual(header_v3, ["total", "dataset_id"])

    def test_check_if_create_header_function_returns_correct_header_v4(self):
        header_v4 = extraction.create_header(self.search_v4)
        self.assertEqual(header_v4, ["total", "dataset_id", "status_text", "status_code"])

    def test_check_if_create_header_function_returns_correct_header_v5(self):
        header_v5 = extraction.create_header(self.search_v5)
        self.assertEqual(header_v5, ["data", "status_text", "status_code"])

    def test_check_if_create_header_function_returns_correct_header_v6(self):
        header_v6 = extraction.create_header(self.search_v6)
        self.assertEqual(header_v6, ["id", "name", "name", "email", "name", "dateCreated"])

    def test_if_get_saved_data_return_correct_results_with_sub_data_relationship_one_to_many(self):
        returned_data = extraction.get_save_data(self.retrieved_data)
        self.assertEqual(returned_data,
                         [{'from_data_1': 'data_1', 'from_data_2': 'data_2', 'from_sub_data_1': 'data_1'}])

    def test_if_get_saved_data_return_correct_one_key_results(self):
        returned_data = extraction.get_save_data(self.retrieved_data_v2)
        self.assertEqual(returned_data, [{'from_list_data_1': 'data_1'}])

    def test_if_extraction_returns_correct_file_name(self):
        csv_file = ""
        extraction.csv_extraction(self.retrieved_data, self.search_retrieve_data, "output_csv")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        for file in os.listdir(dir_path):
            if file.endswith(".csv"):
                csv_file = file
        self.assertEqual(csv_file, "output_csv.csv")
        os.remove(csv_file)
