import random


def capitalize(string):
    return string[:1].upper() + string[1:]


def random_element(xlist):
    return random.choice(xlist) if len(xlist) > 0 else None
