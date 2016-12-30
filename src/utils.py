import random
import re
from typing import List


def capitalize(string: str) -> str:
    return string[:1].upper() + string[1:]


def strings_has_equal_letters(str1: str, str2: str) -> bool:
    def clear_symbols(string):
        return re.sub(r'[\W_]', '', string).lower()

    return clear_symbols(str1) == clear_symbols(str2)


def random_element(xlist: List[object]) -> object:
    return random.choice(xlist) if len(xlist) > 0 else None


def deep_get_attr(obj: object, attr: str, default: object=None):
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = getattr(obj, i)
            if callable(obj):
                obj = obj()
        except AttributeError:
            return default
    return obj


def safe_cast(val: object, to_type: callable, default: object=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default
