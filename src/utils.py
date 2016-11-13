import random
import re


def capitalize(string):
    return string[:1].upper() + string[1:]


def strings_has_equal_letters(str1, str2):
    def clear_symbols(string):
        return re.sub(r'[\W_]', '', string).lower()

    return clear_symbols(str1) == clear_symbols(str2)


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
