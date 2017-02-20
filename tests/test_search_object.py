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

    def test_if_search_object_is_object(self):
        result = search_object.validate(self.searchObject)
        self.assertIsInstance(result, dict)

    def test_if_search_object_is_not_object(self):
        result = search_object.validate(self.wrongSearchObject)
        self.assertFalse(result)

    def test_if_search_object_have_list(self):
        result = search_object.validate_from(self.wrongFromObject)
        self.assertFalse(result)
