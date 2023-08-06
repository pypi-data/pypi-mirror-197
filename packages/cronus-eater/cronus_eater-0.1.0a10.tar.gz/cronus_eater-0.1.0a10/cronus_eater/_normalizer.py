from datetime import datetime
from typing import Any, List

import numpy as np
import pandas as pd

from cronus_eater import _validator
from cronus_eater.exceptions import EmptyDataFrame
from cronus_eater.model import TimeSeries


def norm_blank_value(value: Any) -> Any:
    if _validator.is_blank_value(value):
        return pd.NA

    return value


def norm_header(value: Any) -> Any:
    if isinstance(value, datetime):
        value = f'{pd.Timestamp(value).quarter}T{str(value.year)[2:]}'
        return value

    return value


def norm_df_to_extraction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize a given dataframe to starts the extraction of time series.
    First all blank values are convert to pandas NA values
    Second reset index column
    Third reset the columns if they are not reseted

    :param pd.dataframe df: the dataframe to be normalzied
    :return: a new dataframe ready to start the search for times series
    """

    if df.empty or _validator.is_blank_df(df):
        raise EmptyDataFrame()

    norm_df = df.applymap(lambda value: norm_blank_value(value))
    norm_df = norm_df.T.reset_index(drop=False).T.reset_index(drop=True)

    return norm_df
