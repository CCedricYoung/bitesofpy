import numpy as np
import pandas as pd


def return_at_index(ser: pd.Series, idx: int) -> object:
    """Return the Object at the given index of the Series
    If you want to be extra careful catch and raise an error if
       the index does not exist.
    """
    return ser.iloc[idx]


def get_slice(ser: pd.Series, start: int, end: int) -> pd.core.series.Series:
    """Return the slice of the given Series in the range between
    start and end.
    """
    return ser.iloc[start:end]


def get_slice_inclusive(ser: pd.Series, start: int, end: int) -> pd.core.series.Series:
    """Return the slice of the given Series in the range between
    start and end inclusive.
    """
    end = end != -1 and end + 1 or end
    return ser.iloc[start:end]


def return_head(ser: pd.Series, num: int) -> pd.core.series.Series:
    """Return the first num elements of the given Series."""
    return ser.head(num)


def return_tail(ser: pd.Series, num: int) -> pd.core.series.Series:
    """Return the last num elements of the given Series."""
    return ser.tail(num)


def get_index(ser: pd.Series) -> pd.core.indexes.base.Index:
    """Return all indexes of the given Series."""
    return ser.keys()


def get_values(ser: pd.Series) -> np.ndarray:
    """Return all the values of the given Series."""
    return ser.values


def get_every_second_indexes(ser: pd.Series, even_index=True) -> pd.core.series.Series:
    """Return all rows where the index is either even or odd.
    If even_index is True return every index where idx % 2 == 0
    If even_index is False return every index where idx % 2 != 0
    Assume default indexing i.e. 0 -> n
    """
    start = not even_index and 1 or 0
    return ser.iloc[start::2]
