import unittest

from simpleARS import extraction


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
