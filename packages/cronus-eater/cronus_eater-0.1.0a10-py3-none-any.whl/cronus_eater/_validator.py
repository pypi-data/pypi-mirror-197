import re
from datetime import datetime
from typing import Any, List, Union

import numpy as np
import pandas as pd

from cronus_eater import _converter
from cronus_eater.exceptions import EmptyDataFrame, InvalidDeadLockNumber


def is_blank_value(value: Any) -> bool:
    """
     Verify if a any given value is a blank value.
     A blank value could be: pandas or numpy NA, empty string or string without meaning like -,none, null and nan.

    :param Any value: Any value in pandas dataframe
    :return: A boolean if the value matchs any criteria
    """
    if pd.isnull(value):
        return True

    if len(str(value).strip()) == 0:
        return True

    if str(value).strip().lower() in ('-', 'none', 'null', 'nan'):
        return True

    return False


def is_normal_number(value: str) -> bool:
    if re.match(r'[$]?[\s]?[-]?[\d]+(([.]|[,])[\d]+)?$', value):
        return True

    return False


def is_number_with_comma_sep(value: str) -> bool:
    if re.match(r'[$]?[\s]?[-]?[\d]{1,3}([,][\d]{3})*([.][\d]+)?$', value):
        return True

    return False


def is_number_with_dot_sep(value: str) -> bool:
    if re.match(r'[$]?[\s]?[-]?[\d]{1,3}([.][\d]{3})*([,][\d]+)?$', value):
        return True

    return False


def is_number_with_space_sep(value: str) -> bool:
    if re.match(
        r'[$]?[\s]?[-]?[\d]{1,3}([\s][\d]{3})*(([.]|[,])[\d]+)?$', value
    ):
        return True

    return False


def is_percent_number(value: str) -> bool:
    if re.match(r'[-]?[\d]+(([.]|[,])[\d]+)?[\s]?[%]$', value):
        return True

    return False


def is_number_type(value: Union[float, int, np.number]) -> bool:
    return isinstance(value, (float, int, np.number))


def is_year(value: Any) -> bool:

    if is_blank_value(value):
        return False

    text_value = str(value).strip()
    if re.match(
        r'(([1][9])|([2][0-1]))[0-9][0-9](([.]|[,]|[\s])([0-4]|([0][1-9])|([1][0-2])))?$',
        text_value,
    ):
        return True
    return False


def is_financial_number(value: Any) -> bool:

    if is_blank_value(value):
        return False

    text = str(value).strip()

    if (
        is_normal_number(text)
        or is_number_with_dot_sep(text)
        or is_number_with_comma_sep(text)
        or is_number_with_space_sep(text)
        or is_percent_number(text)
    ):
        return True

    return False


def is_text(value: Any) -> bool:
    return (
        not is_date_time(value)
        and not is_blank_value(value)
        and not is_financial_number(value)
    )


def is_time_series_row(row: pd.Series) -> bool:
    sequence_text: List[str] = []
    sequence_numbers: List[str] = []

    # If is a empty sequence return false
    if len(row.dropna()) == 0:
        return False

    # Calcule the right pattern of a time series row
    for value in row:
        if (is_text(value) or is_date_time(value)) and len(
            sequence_numbers
        ) == 0:
            sequence_text.append(str(value))
        elif is_financial_number(value) and len(sequence_text) in (1, 2, 3):
            sequence_numbers.append(str(value))
        elif (is_text(value) or is_date_time(value)) and len(
            sequence_numbers
        ) > 0:
            break

    # if a sequence is empty means we do not have a time series pattern
    if 0 in (len(sequence_numbers), len(sequence_text)):
        return False

    return True


def is_text_row(row: pd.Series) -> bool:
    # If is a empty sequence return false
    if len(row.dropna()) == 0:
        return False

    # If there is at least one number is not a text row
    n_text = 0
    for value in row:
        if is_text(value) or is_date_time(value):
            n_text += 1

    if n_text >= 3:
        return True

    return False


def is_date_time(value: Any) -> bool:

    if is_blank_value(value):
        return False

    if isinstance(value, datetime) or is_year(value):
        return True

    text = str(value).strip()
    if re.match(
        r'(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2})\b)|(\b(0?[1-9]|1[0-2])[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)$',
        text,
    ):
        return True
    elif re.match(r'[1-4]([Q]|[T])[\s]?[1-2]?[0-9]?[0-9][0-9]$', text):
        return True
    elif re.match(r'[1-12][M][\s]?[1-2]?[0-9]?[0-9][0-9]$', text):
        return True
    elif re.match(
        r'([a-z]|[A-Z]){3}([/]|[|]|[\s]|[-])([0-9]{2})?[0-9]{2}$', text
    ):
        return True

    return False


def is_blank_df(df: pd.DataFrame) -> bool:
    """
    Verify if a dataframe there's just blank values
    :param pd.DataFrame df: dataframe with blank values
    return: A boolean if this df just has blank values
    """
    if df.empty:
        return False
    norm_df = df.applymap(lambda value: _converter.blank_to_na(value))
    return (~norm_df.isna()).values.sum() == 0


def is_there_time_series(df: pd.DataFrame, dead_lock_detector: int) -> bool:
    """
    Verify if there's times series in a given dataframe.

    :param pd.DataFrame df: dataframe where could have one or more a time series
    :param int dead_lock_detector: Number of times which the program could not find a time series in the same area
    :raise EmptyDataFram: if a empty dataframe was passed
    :raise InvalidDeadLockNumber: if negative dead lock is passed
    :return: A boolean if it should continue the search for the time series
    """

    if df.empty:
        raise EmptyDataFrame()

    if dead_lock_detector < 0:
        raise InvalidDeadLockNumber()

    return not is_blank_df(df) and dead_lock_detector in (0, 1)
