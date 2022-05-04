# -*- coding: utf-8 -*-

def is_none_empty(s) -> bool:
    """
    Indicates whether the specified string is null or an empty string ("").
    Visit: https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty
    :param s: string
    :return: True whether the specified string is null or an empty string (""), otherwise False.
    """
    return s is None or "".__eq__(s) or s.isspace()


def is_none_empty_space(s) -> bool:
    """
    Indicates whether a specified string is null, empty, or consists only of white-space characters.
    :param s: string
    :return: True whether the string is null, empty, or consists only of white-space characters, otherwise False.
    """
    return is_none_empty(s) or s.isspace()
