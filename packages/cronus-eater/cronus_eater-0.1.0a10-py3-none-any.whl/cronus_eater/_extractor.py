from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pandas as pd
from typing_extensions import Literal, overload

from cronus_eater import _normalizer, _validator
from cronus_eater.model import TimeSeries, TimeSeriesMetadata


def find_metadata(df: pd.DataFrame, origin: str) -> List[TimeSeriesMetadata]:
    return []


def slice_dataframe(
    df: pd.DataFrame, metadata: List[TimeSeriesMetadata]
) -> List[TimeSeries]:
    return []


def find_header(df: pd.DataFrame, start_row: int, end_column: int) -> int:
    for index, value in df.iloc[start_row - 1 :: -1, end_column].items():
        if _validator.is_date_time(value):
            return int(str(index))

    return -1


def find_end_column(row: pd.Series) -> int:
    last_text_column = -1
    last_number_column = -1

    # If is a empty sequence return false
    if len(row.dropna()) == 0:
        return False

    qtd_text_sequence = 0
    # Calcule the right pattern of a time series row
    for index, value in row.items():
        if (
            _validator.is_text(value) or _validator.is_date_time(value)
        ) and last_number_column == -1:
            last_text_column = int(str(index))
            qtd_text_sequence += 1
        elif _validator.is_financial_number(value) and last_text_column != -1:
            last_number_column = int(str(index))
        elif (
            _validator.is_text(value) or _validator.is_date_time(value)
        ) and last_number_column != -1:
            break

    # if a sequence is empty means we do not have a time series pattern
    if -1 in (last_text_column, last_number_column):
        return -1

    return last_number_column


def find_start_row_index(df: pd.DataFrame, column_index: int) -> int:
    for row_index, row in df.iloc[:, column_index:].iterrows():
        if not pd.isnull(row.iloc[0]):
            if _validator.is_time_series_row(row):
                return int(str(row_index))

    return -1


def find_start_row_column(df: pd.DataFrame) -> Tuple[int, int]:
    for column_index, column in df.items():
        start_column = int(str(column_index))
        if len(column.dropna()) >= 2:
            start_row = find_start_row_index(df, int(str(column_index)))

            if start_row != -1:
                return start_row, start_column

    return -1, -1


def find_end_row_column(
    df: pd.DataFrame, start_row: int, start_column: int
) -> Tuple[int, int]:

    end_column = find_end_column(df.iloc[start_row, start_column:])
    df = df.iloc[start_row:, start_column:end_column].copy()

    end_row = -1
    for row_index, row in df.iterrows():
        if _validator.is_time_series_row(row):
            end_row = int(str(row_index))
        elif _validator.is_text_row(row):
            break

    return end_row, end_column


def clean_garbage_row(row: pd.Series) -> pd.Series:
    qtd_text = row.map(lambda value: _validator.is_text(value)).sum()
    if qtd_text >= 3:
        return row.map(lambda value: pd.NA)
    return row


def to_literal_blank(value: Any) -> Any:
    if pd.isna(value):
        return 'Vazio'
    return value


def clean_time_series_from_raw_df(
    df: pd.DataFrame,
    start_row: int,
    end_row: int,
    start_column: int,
    end_column: int,
) -> pd.DataFrame:
    df.iloc[
        start_row : end_row + 1,
        start_column : end_column + 1,
    ] = np.nan
    return df.copy()


def clean_gargabe_column(
    df: pd.DataFrame, start_row: int, start_column: int
) -> pd.DataFrame:

    if start_row == -1 and start_column >= 0:
        df[df.columns[start_column]] = np.nan
        return df.copy()

    return df.copy()


def clean_gargabe_table(
    df: pd.DataFrame,
    start_row: int,
    start_column: int,
    end_row: int,
    end_column: int,
) -> pd.DataFrame:

    if (
        start_row >= 0
        and start_column >= 0
        and end_column >= 0
        and end_row >= 0
    ):
        df.iloc[start_row : end_row + 1, start_column : end_row + 1] = np.nan
        return df.copy()

    return df.copy()


def extract_raw(raw_dataframe: pd.DataFrame) -> List[pd.DataFrame]:

    df = _normalizer.norm_df_to_extraction(raw_dataframe)

    dfs: List[pd.DataFrame] = []
    dead_lock_detector = 0

    while _validator.is_there_time_series(df, dead_lock_detector):

        start_row, start_column = find_start_row_column(df)

        # If can find start row, but no start_column, clean gargabe column and starts again the search
        if start_row == -1 and start_column >= 0:
            df = clean_gargabe_column(df, start_row, start_column)
            dead_lock_detector += 1
            continue
        # If there's no start row and column ends the search
        elif start_row == -1 and start_column == -1:
            break

        end_row, end_column = find_end_row_column(df, start_row, start_column)

        header_row = find_header(df, start_row, end_column)
        # If can't find a header row clean the table and start again the search
        if header_row == -1:
            df = clean_gargabe_table(
                df, start_row, start_column, end_row, end_column
            )
            dead_lock_detector += 1
            continue
        else:
            start_row = header_row

        # Copy Time Series from raw dataframe
        time_series_df = df.iloc[
            start_row : end_row + 1, start_column : end_column + 1
        ].copy()

        if not time_series_df.empty:
            dfs.append(time_series_df)

        # Clean Time Series from raw dataframe
        df = clean_time_series_from_raw_df(
            df, start_row, end_row, start_column, end_column
        )

    return dfs


def extract_from_dataframe(raw_dataframe: pd.DataFrame) -> pd.DataFrame:
    raw_dfs = extract_raw(raw_dataframe)

    if len(raw_dfs) == 0:
        return pd.DataFrame()

    norm_dfs = []
    for index, time_series_df in enumerate(raw_dfs):
        time_series_df = (
            time_series_df.apply(lambda row: clean_garbage_row(row), axis=1)
            .dropna(how='all', axis=0)
            .dropna(how='all', axis=1)
        )

        time_series_df[time_series_df.columns[0]] = time_series_df[
            time_series_df.columns[0]
        ].map(lambda value: to_literal_blank(value))
        time_series_df = time_series_df.applymap(
            lambda value: _normalizer.norm_blank_value(value)
        )

        time_series_df.iloc[0, 0] = 'Label Index'
        time_series_df.iloc[0, :] = time_series_df.iloc[0, :].map(
            lambda value: _normalizer.norm_header(value)
        )

        time_series_df = time_series_df.rename(
            columns=time_series_df.iloc[0].to_dict()
        ).drop(time_series_df.index[0])

        time_series_df.fillna(0, inplace=True)
        time_series_df.reset_index(inplace=True)
        time_series_df.rename(columns={'index': 'Numeric Index'}, inplace=True)

        time_series_df['Order'] = index + 1

        time_series_df = pd.melt(
            time_series_df,
            id_vars=['Numeric Index', 'Label Index', 'Order'],
            var_name='Time',
            value_name='Value',
        )
        norm_dfs.append(time_series_df.copy())

    return pd.concat(norm_dfs, ignore_index=True)


def extract_from_all_dataframes(
    raw_dataframes: Dict[Union[str, int], pd.DataFrame]
) -> pd.DataFrame:
    all_time_series = []

    for sheet_name, raw_df in raw_dataframes.items():
        df = extract_from_dataframe(raw_df)
        if not df.empty:
            df['Sheet Name'] = sheet_name
            all_time_series.append(df)

    return pd.concat(all_time_series, ignore_index=True)


def extract_from_all_raw_dataframes(
    raw_dataframes: Dict[Union[str, int], pd.DataFrame]
) -> Dict[Union[str, int], List[pd.DataFrame]]:

    all_raw_df: Dict[Union[str, int], List[pd.DataFrame]] = {}

    for sheet_name, raw_df in raw_dataframes.items():
        dfs = extract_raw(raw_df)
        if len(dfs) > 0:
            all_raw_df[sheet_name] = dfs

    return all_raw_df


def extract_many(
    raw_dataframes: Dict[Union[str, int], pd.DataFrame],
    mode: Union[Literal['tidy'], Literal['raw']] = 'tidy',
) -> Union[pd.DataFrame, Dict[Union[str, int], List[pd.DataFrame]]]:
    if mode == 'tidy':
        return extract_from_all_dataframes(raw_dataframes)
    elif mode == 'raw':
        return extract_from_all_raw_dataframes(raw_dataframes)


def extract(
    raw_dataframe: pd.DataFrame,
    mode: Union[Literal['tidy'], Literal['raw']] = 'tidy',
) -> Union[pd.DataFrame, List[pd.DataFrame]]:

    if mode == 'tidy':
        return extract_from_dataframe(raw_dataframe)
    elif mode == 'raw':
        return extract_raw(raw_dataframe)
