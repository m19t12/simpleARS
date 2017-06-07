# coding=utf-8
"""
Search Object classes and functions
for validating and parsing data
"""

__authors__ = 'Manolis Tsoukalas'
__date__ = '2017-1-3'
__version__ = '0.2'


class SearchObjectType(object):
    """
    Search object descriptor for validating search object structure
    """
    __slots__ = ('name', 'type', 'default')

    def __init__(self, name, search_type, default=None):
        self.name = "_" + name
        self.type = search_type
        self.default = default if default else search_type()

    def __get__(self, instance, owner):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Value {} is not a type {}".format(value, self.type))
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Can't delete attribute")


class Validate(object):
    """
    Validate class setting up attribute type for validation
    """
    search_from = SearchObjectType("search_from", dict)
    search_select = SearchObjectType("search_select", list)


def validate(json_object):
    """
    validation method for validating the structure of the search object.
    The structure of the search object must be in json format like this:
    {"from": ["select_1", "select_2", {"sub_from": ["select_1", "select_2"]}]}
    :param json_object: the json search object for validation
    :return: the same json object if everything went ok and no exceptions raised
    """
    validation = Validate()

    validation.search_from = json_object

    for data in json_object:
        validation.search_select = json_object[data]

    return json_object


def get_from(json_object):
    """
    method for getting the from key from the search object
    :param json_object: the search object
    :return: the from key from the search object
    """
    obj_from = ""

    for data in json_object:
        obj_from = data

    return obj_from


def get_select(from_key, json_object):
    """
    method for getting the select keys from the search object
    :param from_key: the from key from json object
    :param json_object: the json object
    :return: an array with keys
    """
    return json_object[from_key]


class SearchObject(object):
    """
    class for the search object.
    this is the class we will use for creating and validating the search object
    so we can get the from key and the select key as class attributes
    """
    __slots__ = ('json_object', 'src_from', 'src_select')

    def __init__(self, json_object):
        self.json_object = validate(json_object)
        self.src_from = get_from(json_object)
        self.src_select = get_select(self.src_from, json_object)
