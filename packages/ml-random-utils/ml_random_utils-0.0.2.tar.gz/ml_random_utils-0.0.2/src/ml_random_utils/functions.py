from functools import reduce
from typing import Sequence, Callable, Any


def compose(*funcs: Sequence[Callable[..., Any]]) -> Callable[..., Any]:
    """
    Composes a list of functions in the order they appear as arguments.

    Arguments:
        funcs: a list of functions to compose. They will be applied in the order they are given.

    Returns:
        a function which applies the function arguments sequentially.
    """
    apply = lambda f, g: lambda x: f(g(x))
    return reduce(apply, funcs[::-1], lambda x: x)
