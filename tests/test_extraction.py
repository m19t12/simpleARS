from tests import BaseARSTestCase
from simple_ars.extraction import list_data


class ExtractionTestCase(BaseARSTestCase):
    def setUp(self):
        super(ExtractionTestCase, self).setUp()

        self.single_search = {"data": [{"records": ['unique_id', 'status', 'address']}, 'total']}
        self.list_search = {"~": ['id', 'name', 'zip_code']}

        self.single_sub_search = {"data": [{"records": [{"weather": ['airport_ref']}, {"languages": ['name']}]}]}
        self.list_sub_search = {"~": [{"users": ['user_id']}, {'attrs': [{'prices': ['max_price']}]}, "name"]}

        self.single_search_key_doesnt_exist = {"data": [{"records": ['foo', 'status', 'address']}, 'total']}
        self.list_search_key_doesnt_exist = {"~": ['bar', 'name', 'zip_code']}

    def test_list_data_functionality(self):
        """Test if method list_data retrieve works properly.
        """
        # -- Test for single json response --
        response = list_data(self.single_response_data, self.single_search)

        # Check if limit 1 is applied because of many to one relationship
        self.assertEqual(len(response), 1)

        # Check if contains the total key
        self.assertEqual(response[0]['total'], 4122)

        # -- Test for single json response with sub keys --
        response = list_data(self.single_response_data, self.single_sub_search)

        # Check if contains the name key.
        self.assertEqual(response[0]['name'], 'Agostiniana Hotel')

        # -- Test for single json response when key doesnt exist.
        response = list_data(self.single_response_data, self.single_search_key_doesnt_exist)

        self.assertEqual(response[0]['foo'], [])

        # -- Test for list json response --
        response = list_data(self.list_response_data, self.list_search)

        # Check if returns correct element number
        self.assertEqual(len(response), 5)

        # -- Test for list data with sub keys --
        response = list_data(self.list_response_data, self.list_sub_search)

        # Check if first element has max_price key
        self.assertEqual(response[0]['max_price'], 2.0)

