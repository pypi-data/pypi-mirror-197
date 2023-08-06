from typing import Callable, Any


def dictify(first: list, second: list) -> dict:
    """
    Returns a dictionary where the entries of first
    are the keys and the entries of second are the values.
    Requires that both lists have the same number of elements.
    If first has duplicate elements, raises ValueError.

    Arguments:
        first: a list of values (will become dictionary keys)
        second: a list of values (will become dictionary values)

    Returns:
        a dict object where elements of first are keys and elements of
        second are values.

    """

    if len(first) != len(second):
        error_msg = (
            "The lengths of the lists must be the same. Found "
            f"len(first) = {len(first)} and len(second) = {len(second)}"
        )
        raise ValueError(error_msg)

    if len(set(first)) != len(first):
        raise ValueError("first contains duplicate elements.")

    return dict(zip(first, second))


def reverse_dict(input_dict: dict) -> dict:
    """
    Returns a dictionary where the keys are the values
    of input_dict, and the values are the keys of input_dict.

    Arguments:
        input_dict: the dictionary to reverse

    Returns:
        a dict object where keys are swapped with values and vice-versa.
    """

    return {v: k for (k, v) in input_dict.items()}


def filter_keys(input_dict: dict, condition: Callable[..., bool]) -> dict:
    """
    Returns a dictionary where the entries respect condition
    (applied to the keys).

    Arguments:
        input_dict: the dictionary whose keys will be filtered
        condition: a function that returns a boolean when applied to a dictionary key

    Returns:
        a dict object where only keys for which condition is True are kept.
    """

    return {k: v for (k, v) in input_dict.items() if condition(k)}


def filter_values(input_dict: dict, condition: Callable[..., bool]) -> dict:
    """
    Returns a dictionary where the entries respect condition
    (applied to the values).

    Arguments:
        input_dict: the dictionary whose values will be filtered
        condition: a function that returns a boolean when applied to a dictionary value

    Returns:
        a dict object where only values for which condition is True are kept.
    """

    return {k: v for (k, v) in input_dict.items() if condition(v)}


def find_nested(input_dict: dict, dotted_path: str) -> Any:
    """
    Recursively traverses input_dict using a dotted path.

    Arguments:
        input_dict: the nested dictionary to be traversed
        dotted_path: a string where each nested key is separated by a dot.

    Returns:
        the value found according to the nested path

    Raises:
        KeyError if the value isn't found.

    """
    if dotted_path.endswith("."):
        raise ValueError(f"dotted path {dotted_path} is badly formatted.")

    keys = dotted_path.split(".")

    if len(keys) <= 1:
        return input_dict[keys[0]]

    return find_nested(input_dict[keys[0]], ".".join(keys[1:]))
