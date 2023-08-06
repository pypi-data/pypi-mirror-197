import itertools
from typing import Callable


def flatten(nested_list: list[list]) -> list:
    """
    Flattens a list of lists into a single list.

    Arguments:
        nested_list (list): a list of lists.

    Returns:
        the input list flattened as a single list.
    """
    return list(itertools.chain.from_iterable(nested_list))


def filter_list(elem_list: list, condition: Callable[..., bool]) -> list:
    """
    Filters a list according to some condition.

    Arguments:
        elem_list (list): the list to filter
        condition (Callable): a function that gets applied to each
                              element of the list and returns a boolean.
    Returns:
        a list where only the elements for which condition returns True are present.
    """
    return [elem for elem in elem_list if condition(elem)]


def intersection(first: list, second: list) -> list:
    """
    Returns the intersection of two lists.

    Arguments:
        first: the first list
        second: the second list

    Returns:
        the list containing the intersection of the two lists.
    """
    return list(set(first).intersection(set(second)))


def difference(first: list, second: list) -> list:
    """
    Returns the difference of two lists.

    Arguments:
        first: the first list
        second: the second list

    Returns:
        the list containing the difference of the two lists.
    """
    return list(set(first).difference(set(second)))


def union(first: list, second: list) -> list:
    """
    Returns the union of two lists.

    Arguments:
        first: the first list
        second: the second list

    Returns:
        the list containing the union of the two lists.
    """
    return list(set(first).union(set(second)))
