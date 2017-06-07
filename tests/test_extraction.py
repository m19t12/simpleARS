# coding=utf-8
from tests import BaseARSTestCase


class ExtractionTestCase(BaseARSTestCase):
    def setUp(self):
        super(ExtractionTestCase, self).setUp()

        self.single_search = {"data": [{"records": ['unique_id', 'status', 'address']}, 'total']}
        self.list_search = {"~": ['id', 'name', 'zip_code']}

        self.single_sub_search = {"data": [{"records": [{"weather": ['airport_ref']}, {"languages": ['name']}]}]}
        self.list_sub_search = {"~": [{"users": ['user_id']}, {'attrs': [{'prices': ['max_price']}]}, "name"]}

        self.single_search_key_doesnt_exist = {"data": [{"records": ['foo', 'status', 'address']}, 'total']}
        self.list_search_key_doesnt_exist = {"~": ['bar', 'name', 'zip_code']}
