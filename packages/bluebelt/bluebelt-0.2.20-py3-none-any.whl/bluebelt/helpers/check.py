import pandas as pd
import numpy as np

NoneType = type(None)

def is_int(*args):
    if not all([isinstance(arg, int) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, int)])
        raise ValueError(f'The object is expected to be a integer, not {types}')

def is_int_or_none(*args):
    if not all([isinstance(arg, (int, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, int)])
        raise ValueError(f'The object is expected to be a integer, not {types}')

def is_float(*args):
    if not all([isinstance(arg, float) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, float)])
        raise ValueError(f'The object is expected to be a float, not {types}')

def is_float_or_none(*args):
    if not all([isinstance(arg, (float, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, float)])
        raise ValueError(f'The object is expected to be a float, not {types}')

def is_boolean(*args):
    if not all([isinstance(arg, bool) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, bool)])
        raise ValueError(f'The object is expected to be a boolean, not {types}')

def is_boolean_or_none(*args):
    if not all([isinstance(arg, (bool, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, bool)])
        raise ValueError(f'The object is expected to be a boolean, not {types}')

def is_str(*args):
    if not all([isinstance(arg, str) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, str)])
        raise ValueError(f'The object is expected to be a string, not {types}')

def is_str_or_none(*args):
    if not all([isinstance(arg, (str, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, str)])
        raise ValueError(f'The object is expected to be a string, not {types}')

def is_list(*args):
    if not all([isinstance(arg, list) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, list)])
        raise ValueError(f'The object is expected to be a list, not {types}')

def is_list_or_none(*args):
    if not all([isinstance(arg, (list, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, list)])
        raise ValueError(f'The object is expected to be a list, not {types}')

def is_tuple(*args):
    if not all([isinstance(arg, tuple) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, tuple)])
        raise ValueError(f'The object is expected to be a tuple, not {types}')

def is_tuple_or_none(*args):
    if not all([isinstance(arg, (tuple, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, tuple)])
        raise ValueError(f'The object is expected to be a tuple, not {types}')

def is_array(*args):
    if not all([isinstance(arg, np.ndarray) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, np.ndarray)])
        raise ValueError(f'The object is expected to be a numpy ndarray, not {types}')
    
def is_array_or_none(*args):
    if not all([isinstance(arg, (np.ndarray, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, np.ndarray)])
        raise ValueError(f'The object is expected to be a numpy ndarray, not {types}')
    
def is_list_or_tuple(*args):
    if not all([isinstance(arg, (list, tuple)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, (list, tuple))])
        raise ValueError(f'The object is expected to be a list or a tuple, not {types}')
is_tuple_or_list = is_list_or_tuple

def is_list_or_tuple_or_none(*args):
    if not all([isinstance(arg, (list, tuple, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, (list, tuple))])
        raise ValueError(f'The object is expected to be a list or a tuple, not {types}')
is_tuple_or_list_or_none = is_list_or_tuple_or_none


def is_list_or_tuple_or_array(*args):
    if not all([isinstance(arg, (list, tuple, np.ndarray)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, (list, tuple, np.ndarray))])
        raise ValueError(f'The object is expected to be a list, tuple or numpy ndarray, not {types}')
is_list_or_array_or_tuple = is_list_or_tuple_or_array
is_tuple_or_list_or_array = is_list_or_tuple_or_array
is_tuple_or_array_or_list = is_list_or_tuple_or_array
is_array_or_tuple_or_list = is_list_or_tuple_or_array
is_array_or_list_or_tuple = is_list_or_tuple_or_array

def is_list_or_tuple_or_array_or_none(*args):
    if not all([isinstance(arg, (list, tuple, np.ndarray, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, (list, tuple, np.ndarray))])
        raise ValueError(f'The object is expected to be a list, tuple or numpy ndarray, not {types}')
is_list_or_array_or_tuple_or_none = is_list_or_tuple_or_array_or_none
is_tuple_or_array_or_list_or_none = is_list_or_tuple_or_array_or_none
is_array_or_tuple_or_list_or_none = is_list_or_tuple_or_array_or_none
is_array_or_list_or_tuple_or_none = is_list_or_tuple_or_array_or_none

def is_dict(*args):
    if not all([isinstance(arg, dict) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, dict)])
        raise ValueError(f'The object is expected to be a dictionary, not {types}')

def is_dict_or_none(*args):
    if not all([isinstance(arg, (dict, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, dict)])
        raise ValueError(f'The object is expected to be a dictionary, not {types}')

def is_series(*args):
    if not all([isinstance(arg, pd.Series) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.Series)])
        raise ValueError(f'The object is expected to be a pandas Series, not {types}')

def is_series_or_none(*args):
    if not all([isinstance(arg, (pd.Series, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.Series)])
        raise ValueError(f'The object is expected to be a pandas Series, not {types}')

def is_frame(*args):
    if not all([isinstance(arg, pd.DataFrame) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.DataFrame)])
        raise ValueError(f'The object is expected to be a pandas DataFrame, not {types}')

def is_frame_or_none(*args):
    if not all([isinstance(arg, (pd.DataFrame, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.DataFrame)])
        raise ValueError(f'The object is expected to be a pandas DataFrame, not {types}')

def is_series_or_frame(*args):
    if not all([isinstance(arg, (pd.Series, pd.DataFrame)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, (pd.Series, pd.DataFrame))])
        raise ValueError(f'The object is expected to be a pandas Series or DataFrame, not {types}')
is_frame_or_series = is_series_or_frame

def is_series_or_frame_or_none(*args):
    if not all([isinstance(arg, (pd.Series, pd.DataFrame, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, (pd.Series, pd.DataFrame))])
        raise ValueError(f'The object is expected to be a pandas Series or DataFrame, not {types}')
is_frame_or_series_or_none = is_series_or_frame_or_none

def is_index(*args):
    if not all([isinstance(arg, pd.Index) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.Index)])
        raise ValueError(f'The object is expected to be a pandas Index, not {types}')

def is_index_or_none(*args):
    if not all([isinstance(arg, (pd.Index, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.Index)])
        raise ValueError(f'The object is expected to be a pandas Index, not {types}')

def is_datetimeindex(*args):
    if not all([isinstance(arg, pd.DatetimeIndex) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.DatetimeIndex)])
        raise ValueError(f'The object is expected to be a pandas DatetimeIndex, not {types}')

def is_datetimeindex_or_none(*args):
    if not all([isinstance(arg, (pd.DatetimeIndex, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.DatetimeIndex)])
        raise ValueError(f'The object is expected to be a pandas DatetimeIndex, not {types}')

def is_multiindex(*args):
    if not all([isinstance(arg, pd.MultiIndex) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.MultiIndex)])
        raise ValueError(f'The object is expected to be a pandas MultiIndex, not {types}')

def is_multiindex_or_none(*args):
    if not all([isinstance(arg, (pd.MultiIndex, NoneType)) for arg in args]):
        types = ', '.join([type(arg).__name__ for arg in args if not isinstance(arg, pd.MultiIndex)])
        raise ValueError(f'The object is expected to be a pandas MultiIndex, not {types}')

def has_datetimeindex(*args):
    if not all([isinstance(arg.index, pd.DatetimeIndex) for arg in args]):
        types = ', '.join([type(arg.index).__name__ for arg in args if not isinstance(arg.index, pd.DatetimeIndex)])
        raise ValueError(f'The object is expected to have a pandas DateTimeIndex, not {types}')

def has_multiindex(*args):
    if not all([isinstance(arg.index, pd.MultiIndex) for arg in args]):
        types = ', '.join([type(arg.index).__name__ for arg in args if not isinstance(arg.index, pd.MultiIndex)])
        raise ValueError(f'The object is expected to have a MultiIndex, not {types}')