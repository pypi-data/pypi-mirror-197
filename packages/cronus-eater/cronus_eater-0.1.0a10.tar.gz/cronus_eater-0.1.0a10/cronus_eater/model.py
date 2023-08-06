from dataclasses import dataclass

import pandas as pd


@dataclass
class TimeSeriesMetadata:
    alias: str
    origin: str
    start_column: int
    end_column: int
    start_row: int
    end_row: int


@dataclass
class TimeSeries:
    metadata: TimeSeriesMetadata
    dataframe: pd.DataFrame
