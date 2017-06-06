# coding=utf-8
from simple_ars.core import ars, retrieve_data
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

        # -- Test for list response --
        response = ars(self.list_response_data, self.list_search)

        # Check if list response first element contains the id key
        first_element = response[0]
        self.assertEqual(first_element['id'], 70029)

        # Check if list response second element contains the id key
        second_element = response[1]
        self.assertEqual(second_element['id'], 70023)

        # Test sub data retrieval in list json response
        response = ars(self.list_response_data, self.list_sub_search)

        # Check if first element returns users user id key correct
        first_element = response[0]['users']
        self.assertEqual(first_element[0]['user_id'], '1')

        # Check if second element returns users user id key correct
        second_element = response[1]['users']
        self.assertEqual(second_element, [])

        # Check if first element returns None type attrs empty dictionary
        first_element = response[0]['attrs']
        self.assertEqual(first_element, {})

        # Test if key doesnt exist in list response
        response = ars(self.list_response_data, self.list_search_key_doesnt_exist)

        # Check if key doesnt exist in list response first element
        first_element = response[0]
        self.assertEqual(first_element['bar'], None)

        # Test if ARS raises TypeError when we give wrong Response Type
        with self.assertRaises(TypeError):
            ars(self.wrong_type_response, "")

    def test_retrieve_data_functionality(self):
        """
        Test if retrieve data method works properly
        """
        # -- Test for list json response --
        response = retrieve_data(api_url=self.cms_api, credentials=self.credentials, search=self.list_search)

        # Check if first element has key id
        first_element = response[0]
        self.assertEqual(first_element['id'], 70546)

        # Check if first element has key name
        self.assertEqual(first_element['name'], 'St.Thomas Villas Resort')

        # Test for sub data list response
        response = retrieve_data(api_url=self.cms_api, credentials=self.credentials, search=self.list_sub_search)

        # Check if first element has key prices
        first_element = response[0]['attrs']['prices']
        self.assertEqual(first_element['max_price'], 2)

        # -- Test for single json response --
        response = retrieve_data(api_url=self.service_api, search=self.single_search)

        # Check if first element has key unique_id
        first_element = response['records'][0]
        self.assertEqual(first_element['unique_id'], 58788)

        # -- Test export single json response to csv functionality --
        response = retrieve_data(api_url=self.service_api, search=self.single_search, mode='csv',
                                 csv_file_name='output')

        # Check if csv contains total column
        self.assertEqual(response[0]['total'], 4119)

        # -- Test export list json response to csv functionality --
        response = retrieve_data(api_url=self.cms_api, credentials=self.credentials, search=self.list_search,
                                 mode='csv',
                                 csv_file_name='output')

        # Check if first item in csv contains the name column
        self.assertEqual(response[0]['name'], 'St.Thomas Villas Resort')

        # Check if second item in csv contains the name column
        self.assertEqual(response[1]['name'], 'Monambeles Villas')

        # -- Test export list with sub data to csv functionality --
        response = retrieve_data(api_url=self.cms_api, credentials=self.credentials, search=self.list_sub_search,
                                 mode='csv',
                                 csv_file_name='output')

        # Check if first item in csv contains the max_price column
        self.assertEqual(response[0]['max_price'], 2.0)

        # Check if first item doesnt have user
        self.assertEqual(response[0]['user_id'], [])

        # -- Test if we give unknown mode that returns only the processed data --
        response = retrieve_data(api_url=self.service_api, search=self.single_search, mode='foo',
                                 csv_file_name='output')

        # Check if processed data contains total
        self.assertEqual(response['total'], 4119)
