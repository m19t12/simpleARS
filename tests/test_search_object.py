import unittest

from simpleARS import search_object


class SearchObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.searchObject = {
            "from": ["select_1", "select_2"]
        }
        self.wrongSearchObject = "from"
        self.wrongFromObject = {
            "from": "select_1"
        }

    def test_if_validator_raises_type_error_on_wrong_select(self):
        with self.assertRaises(TypeError):
            search_object.validate(self.wrongFromObject)

    def test_if_validator_raises_type_error_on_wrong_search_object(self):
        with self.assertRaises(TypeError):
            search_object.validate(self.wrongSearchObject)

    def test_if_validator_returns_the_same_object(self):
        self.assertEqual(search_object.validate(self.searchObject), self.searchObject)

    def test_if_search_object_returns_from_key_value(self):
        self.assertEqual(search_object.get_from(self.searchObject), "from")

    def test_if_search_object_select_returns_an_array(self):
        self.assertIsInstance(search_object.get_select("from", self.searchObject), list)

    def test_if_search_object_select_returns_the_proper_list(self):
        self.assertEqual(search_object.get_select("from", self.searchObject), ["select_1", "select_2"])
