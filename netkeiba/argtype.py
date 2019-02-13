from argparse import ArgumentTypeError
from datetime import datetime


def date_string(string):
    try:
        datetime.strptime(string, '%Y-%m-%d')
    except TypeError as e:
        raise ArgumentTypeError(e)
    return string
