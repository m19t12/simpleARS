def validate(search_object):
    if isinstance(search_object, dict):
        return validate_from(search_object)
    else:
        return False


def validate_from(search_object):
    from_key = list(search_object.keys())[0]
    if isinstance(search_object[from_key], list):
        return search_object
    else:
        return False
