from functools import wraps
from typing import Callable

import pandas as pd


def rebuild_index(func: Callable[..., pd.DataFrame]) -> Callable[..., pd.DataFrame]:
    """
    Decorator that resets the index of a dataframe and drops it.

    Args:
        func (Callable): any function that returns a pd.DataFrame

    Returns:
        a function whose return value is a pd.DataFrame with the index reset.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> pd.DataFrame:
        dataframe = func(*args, **kwargs)
        return dataframe.reset_index(drop=True)

    return wrapper
