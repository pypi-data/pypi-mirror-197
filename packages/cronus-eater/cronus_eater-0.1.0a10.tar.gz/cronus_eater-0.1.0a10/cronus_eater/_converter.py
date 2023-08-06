from typing import Any

import pandas as pd

from cronus_eater import _validator


def blank_to_zero(value: Any) -> Any:
    """
    Converts any blank value to zero.

    :param Any value: The value to verify if is blank
    :return: if is blank returns 0 else returns the same value
    """
    if _validator.is_blank_value(value):
        return 0

    return value


def blank_to_na(value: Any) -> Any:
    """
    Converts any blank value to pandas NA.

    :param Any value: The value to verify if is blank
    :return: if is blank returns pd.NA else returns the same value
    """
    if _validator.is_blank_value(value):
        return pd.NA

    return value
