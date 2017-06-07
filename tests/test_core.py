# coding=utf-8
from simple_ars.core import ars
from tests import BaseARSTestCase


class CoreTestCase(BaseARSTestCase):
    def setUp(self):
        super(CoreTestCase, self).setUp()

        self.single_search = {"data": [{"records": ['unique_id', 'status', 'address']}, 'total']}
        self.list_search = {"~": ['id', 'name', 'zip_code']}

        self.single_sub_search = {"data": [{"records": [{"weather": ['airport_ref']}, {"languages": ['name']}]}]}
        self.list_sub_search = {"~": [{"users": ['user_id']}, {'attrs': [{'prices': ['max_price']}]}, "name"]}

        self.single_search_key_doesnt_exist = {"data": [{"records": ['foo', 'status', 'address']}, 'total']}
        self.list_search_key_doesnt_exist = {"~": ['bar', 'name', 'zip_code']}

        self.single_search_root = {"~": ['status_text', 'status_code']}

    def test_ars_functionality(self):
        """Test if method ars works properly
        """
        # -- Test for single json response --
        response = ars(self.single_response_data, self.single_search)

        # Check if single response contains the total key
        self.assertEqual(response['total'], 4122)

        # Check if single response contain the first items unique_id key
        first_element = response['records'][0]
        self.assertEqual(first_element['unique_id'], 58788)

        # Check if single response contain the second items unique_id key
        second_element = response['records'][1]
        self.assertEqual(second_element['unique_id'], 58789)

        # Test sub data retrieval in single json response
        response = ars(self.single_response_data, self.single_sub_search)

        # Check if first element contains the weather airport_ref key
        first_element = response['records'][0]['weather']
        self.assertEqual(first_element['airport_ref'], 'Reggio Calabria (LICR)')

        # Check if second element contains the weather airport_ref key
        second_element = response['records'][1]['weather']
        self.assertEqual(second_element['airport_ref'], 'Luqa (LMML)')

        # Check if first element contains the first languages name key
        first_element = response['records'][0]['languages']
        self.assertEqual(first_element[0]['name'], 'Agostiniana Hotel')

        # Check if second element contains the first languages name key
        second_element = response['records'][1]['languages']
        self.assertEqual(second_element[0]['name'], 'Riviera Resort & Spa')

        # Check if forth which contains more languages returns properly the second languages name key
        fourth_element = response['records'][3]['languages']
        self.assertEqual(fourth_element[1]['name'], 'Aldiola Country Resort')

        # Test if key doesnt exist in single response json
        response = ars(self.single_response_data, self.single_search_key_doesnt_exist)

        # Check if key doesnt exist in single json response first element
        first_element = response['records'][0]
        self.assertEqual(first_element['foo'], None)

        # Check if key doesnt exist in single json response second element
        second_element = response['records'][1]
        self.assertEqual(second_element['foo'], None)

        # -- Test single json response retrieve from root
        response = ars(self.single_response_data, self.single_search_root)

        # Check if response contains the status_code key
        self.assertEqual(response['status_code'], 200)

        # -- Test for list response --
        response = ars(self.list_response_data, self.list_search)

        # Check if list response first element contains the id key
        first_element = response[0]
        self.assertEqual(first_element['id'], 70546)

        # Check if list response second element contains the id key
        second_element = response[1]
        self.assertEqual(second_element['id'], 70561)

        # Test sub data retrieval in list json response
        response = ars(self.list_response_data, self.list_sub_search)

        # Check if last element returns users user id key correct
        last_element = response[4]['users']

        self.assertEqual(last_element[0]['user_id'], '5568')

        # Check if second element returns users user id key correct
        second_element = response[1]['users']
        self.assertEqual(second_element, [])

        # Test if key doesnt exist in list response
        response = ars(self.list_response_data, self.list_search_key_doesnt_exist)

        # Check if key doesnt exist in list response first element
        first_element = response[0]
        self.assertEqual(first_element['bar'], None)

        # Test if ARS raises TypeError when we give wrong Response Type
        with self.assertRaises(TypeError):
            ars(self.wrong_type_response, "")
