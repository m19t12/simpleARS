# coding=utf-8
from simple_ars.extraction import ars_list
from tests import BaseARSTestCase


class ExtractionTestCase(BaseARSTestCase):
    def setUp(self):
        super(ExtractionTestCase, self).setUp()

        self.single_search = {"data": [{"records": ['unique_id', 'status', 'address']}, "total"]}
        self.list_search = {"~": ['id', 'name', 'zip_code']}

        self.single_sub_search = {"data": [{"records": [{"weather": ['airport_ref']}, {"languages": ['name']}]}]}
        self.list_sub_search = {"~": [{"users": ['user_id']}, {'attrs': [{'prices': ['max_price']}]}, "name"]}

        self.single_search_key_doesnt_exist = {"data": [{"records": ['foo', 'status', 'address']}, 'total']}
        self.list_search_key_doesnt_exist = {"~": ['bar', 'name', 'zip_code']}

    def test_ars_list(self):
        """test if method ars_list works properly
        """
        # -- Test in single response data --
        response = ars_list(self.single_response_data, self.single_search)

        # check if single json response contains 2 values
        self.assertEqual(len(response), 11)

        # check if contains the key total
        self.assertEqual(response[10]['total'], 4122)

        # check if contains the sub data
        first_element = response[0]
        self.assertEqual(first_element['status'], "ready")

        # -- Test single json sub search --
        response = ars_list(self.single_response_data, self.single_sub_search)

        # Check if first element contains the name key
        first_element = response[0]
        self.assertEqual(first_element['name'], 'Agostiniana Hotel')

        # -- Test list json search --
        response = ars_list(self.list_response_data, self.list_search)

        # Check if first element contains the key id
        first_element = response[0]
        self.assertEqual(first_element['id'], 70546)

        # -- Test list json sub search --
        response = ars_list(self.list_response_data, self.list_sub_search)

        # Check if first element has max_price
        first_element = response[0]
        self.assertEqual(first_element['max_price'], 2.0)
