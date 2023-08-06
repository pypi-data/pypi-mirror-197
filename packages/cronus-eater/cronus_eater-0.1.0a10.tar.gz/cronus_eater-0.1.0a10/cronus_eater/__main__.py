import string
from typing import Dict, List, Union

import pandas as pd
from loguru import logger
from unidecode import unidecode

import cronus_eater
from cronus_eater import _converter


def main():
    logger.info('Reading File ...')
    raw_dataframes = pd.read_excel(
        'tests/integration/data/nubank_3Q22.xlsx', header=None, sheet_name=None
    )

    logger.info('Processing Time Series ...')
    times_series_df = cronus_eater.extract_many(raw_dataframes, mode='tidy')

    norm_index = (
        times_series_df['Label Index']
        .str.strip()
        .map(
            lambda value: unidecode(
                str(value).translate(str.maketrans('', '', string.punctuation))
            )
        )
        .str.replace(' ', '_')
    )

    norm_sheet_name = (
        times_series_df['Sheet Name']
        .str.strip()
        .map(
            lambda value: unidecode(
                str(value).translate(str.maketrans('', '', string.punctuation))
            )
        )
        .str.replace(' ', '_')
    )

    times_series_df['Chave'] = (
        norm_sheet_name
        + '_'
        + times_series_df['Numeric Index'].astype(str)
        + '_'
        + times_series_df['Order'].astype(str)
        + '_'
        + norm_index
    )

    times_series_df = times_series_df.pivot_table(
        index=['Chave'],
        columns='Time',
        values='Value',
    ).applymap(lambda value: _converter.blank_to_zero(value))

    times_series_df = times_series_df.reindex(
        sorted(times_series_df.columns.values, key=lambda value: value[1:]),
        axis=1,
    ).reset_index()

    logger.info('Saving Data ...')
    times_series_df.to_excel('xablau.xlsx', index=False)


if __name__ == '__main__':
    main()
