def capitalize(string):
    return string[:1].upper() + string[1:]


def deep_get_attr(obj, attr, default=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
            if callable(obj):
                obj = obj()
        except AttributeError:
            return default
    return obj


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def read_to_string(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data
