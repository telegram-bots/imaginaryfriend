import random


def capitalize(string):
    return string[:1].upper() + string[1:]


def random_element(xlist):
    return random.choice(xlist) if len(xlist) > 0 else None


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
