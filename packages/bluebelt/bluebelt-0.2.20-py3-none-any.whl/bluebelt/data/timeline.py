import pandas as pd
import numpy as np

import datetime
import itertools
import math

import bluebelt.helpers.check as check
import bluebelt.helpers.convert

NoneType = type(None)


def from_dataframe(_obj, start=None, end=None, value=None, **kwargs):
    """
    Create a pandas Series timeline from a pandas DataFrame

    Parameters
    ----------
    _obj: the pandas DataFrame
    start: the column name with the start Timestamp data, default None
    end: the column name with the end Timestamp data, default None
    value: the columns with the value data, default None

    Returns
    -------
    The new pandas Series object

    """
    check.is_frame(_obj)
    check.is_str(start, end)
    check.is_str_or_none(value)

    # remove rows with start == end
    # remove NaT values
    _obj = _obj[_obj[start] != _obj[end]]
    _obj = _obj[~(_obj[start].isna() | _obj[end].isna())]

    # set new index
    index = pd.Index(_obj[start].values).union(pd.Index(_obj[end].values))

    # build input series
    if value:
        series = _obj.groupby([start, end])[value].sum().rename("value")
    else:
        series = _obj.groupby([start, end])[start].count().rename("value")

    # remove start == end
    series = series[
        series.index.get_level_values(0) != series.index.get_level_values(1)
    ]

    # remove NaT
    series = series[~series.isna()]

    # start with an empty array
    array = np.zeros(index.size)

    # add each row of the series to the array
    for key, value in series.to_dict().items():
        array = np.add(
            array,
            np.multiply(
                ((index.values >= key[0]) & (index.values < key[1])).astype(float),
                value,
            ),
        )

    result = pd.Series(index=index, data=array)

    # remove duplicate indices
    result = result[~result.index.duplicated(keep="first")]

    return result


def add_series(_obj, other=None, **kwargs):
    """
    Add data to pandas Series to build a timeline.

    Parameters
    ----------
    _obj: the pandas Series object
    other: the pandas Series to add, default None

    Returns
    -------
    The new pandas Series object

    """
    check.is_series(other)

    # build new index
    index = _obj.index.union(other.index)

    # reindex to new index
    t1 = _obj.reindex(index).ffill().fillna(0)
    t2 = other.reindex(index).ffill().fillna(0)

    return t1.add(t2)


def add_dataframe(_obj, other=None, start=None, end=None, value=None, **kwargs):
    """
    Add data to pandas Series to build a timeline.

    Parameters
    ----------
    _obj: the pandas Series
    other: the pandas DataFrame to add
    start: the column name with the start Timestamp data, default None
    end: the column name with the end Timestamp data, default None
    value: the columns with the value data, default None

    Returns
    -------
    The new pandas Series object

    """
    check.is_frame(other)
    check.is_str(start, end, value)

    other = from_dataframe(other, start=start, end=end, value=value, **kwargs)
    return _obj.reindex(other.index).ffill().fillna(0).add(other)


add_frame = add_dataframe


def add_list(_obj, other, **kwargs):
    """
    Add data to pandas Series to build a timeline.

    Parameters
    ----------
    _obj: the pandas series
    other: the object to add, default None
        The object must be a list, a tuple or a numpy ndarray.
        The first two items in the list must be or be convertible to
        Pandas Timestamps. If the list has a third item the value will
        be the third items value, if not it will be 1.
        
    Returns
    -------
    The new pandas Series object

    """
    check.is_list_or_tuple_or_array(other)

    # check if there are at least two timestamps or force an error
    start = pd.Timestamp(other[0])
    end = pd.Timestamp(other[1])

    # set value
    value = other[2] if len(other) > 2 else 1

    other_index = pd.Index([start, end], dtype="datetime64[ns]")
    new_index = _obj.index.union(other_index)

    # reindex the series
    t1 = _obj.reindex(new_index).ffill().fillna(0)
    t2 = (
        pd.Series(index=other_index, data=[value, 0],)
        .reindex(new_index)
        .ffill()
        .fillna(0)
    )

    return t1.add(t2)


add_tuple = add_list
add_array = add_list


def add_dict(_obj, other, **kwargs):
    """
    Add data to pandas Series to build a timeline.

    Parameters
    ----------
    _obj: the pandas series
    other: the dict to add, default None
        The dict must have the keys 'start' and 'end' that have Pandas
        Timestamp-like values If the 'value' key is not in the dict the
        value will be 1.
        
    Returns
    -------
    The new pandas Series object
    """

    check.is_dict(other)

    # check if there are at least two timestamps or force an error
    start = pd.Timestamp(other.get("start"))
    end = pd.Timestamp(other.get("end"))
    value = other.get("value", 1)

    other_index = pd.Index([start, end], dtype="datetime64[ns]")
    new_index = _obj.index.union(other_index)

    # reindex the Timeline objects (returns pd.Series objects)
    t1 = _obj.reindex(new_index).ffill().fillna(0)
    t2 = (
        pd.Series(index=other_index, data=[value, 0],)
        .reindex(new_index)
        .ffill()
        .fillna(0)
    )

    return t1.add(t2)


def add(_obj, other=None, start=None, end=None, value=None, **kwargs):
    """
    Add data to pandas Series to build a timeline.

    Parameters
    ----------
    _obj: the pandas series
    other: the object to add, default None
        If the object is a pandas Series a new Series is created with
        a combined index.
        If the object is a Pandas Dataframe and 'start' and 'end' are
        provided every row in the dataframe is added to the timeline. A
        'value' column is optional.
        If the object is a tuple or list and the first two items in it are
        Pandas Timestamps or can be converted to Pandas Timestamps a new
        object is created with a combined index. If a third item is given
        the value will be the third items value, if not it will be 1.
        If the object is a dict with keys 'start' and 'end' that have
        Pandas Timestamp-like values a new object is created with a combined
        index. If a 'value' key is not in the dict the value will be 1.
        If the object is a Pandas Series of int the default Pandas add
        function is used.
    start: the column name with the start Timestamp data, default None
        Only used if 'other' is a Pandas DataFrame
    end: the column name with the end Timestamp data, default None
        Only used if 'other' is a Pandas DataFrame
    value: the columns with the value data, default None
        Only used if 'other' is a Pandas DataFrame

    Returns
    -------
    The new pandas Series object

    """
    if isinstance(other, pd.Series):
        return add_series(_obj, other)

    elif isinstance(other, (list, tuple, dict, np.ndarray)):
        return add_array(_obj, other)

    elif (
        isinstance(other, pd.DataFrame, start=start, end=end, value=value)
        and start is not None
        and end is not None
    ):
        return add_dataframe(_obj, other)

    else:
        return _obj


def get_shifts(
    _obj, shifts=None, adjust_midnight=0, freq=None, *args, **kwargs,
):
    """
    Get the ideal combination of shifts for a given timeline.

    Parameters
    ----------
    _obj: the pandas series
    shifts: a list of shift lengths in hours, default None
        A list of possible shift lengths can be passed in any order.
        e.g. [8, 6, 3, 4]
        Another option is to pass a list of pandas Timedelta values.
        e.g. [pandas.Timedelta('8h'), pandas.Timedelta('4.5h')]
    freq: the frequency to use in the timeline
    adjust_midnight: adjust midnight in hours, default 0
        Every next iso day will start at midnight + adjust_midnight hours.
        e.g. adjust_midnight = -1 => the next iso day starts at 23:00

    Returns
    -------
    A new pandas DataFrame with all the shifts.

    """

    if isinstance(_obj.index, pd.MultiIndex) and all(
        [x in _obj.index.names for x in ["day", "hour", "minute"]]
    ):
        _obj.index = _obj.index.map(
            lambda x: datetime.datetime.combine(
                datetime.date.fromisocalendar(1973, 16, x[0]), datetime.time(x[1], x[2])
            )
        )
        _obj.index.freq = min(_obj.index[1:] - _obj.index[:-1])
    elif not isinstance(_obj.index, pd.DatetimeIndex):
        raise ValueError(
            f"Index must be a DatetimeIndex or MultiIndex with 'day', 'hour' and 'minute' not {type(_obj.index).__name__}."
        )

    freq = freq or pd.Timedelta(_obj.index.freq.freqstr)
    adjust = int(pd.Timedelta(f"{-adjust_midnight} hours") / freq)

    result = {}

    # make sure shifts is a list of pd.Timedelta
    if all([isinstance(x, (int, float)) for x in shifts]):
        shifts = [pd.Timedelta(f"{x} hours") for x in shifts]

    # loop years
    for year in _obj.index.isocalendar().year.unique():
        result[year] = {}

        # loop weeks
        for week in _obj.index.isocalendar().week.unique():
            result[year][week] = {}

            # loop weekdays
            for day in _obj.index.isocalendar().day.unique():
                arr = _obj.shift(adjust)[
                    (_obj.index.isocalendar().year == year)
                    & (_obj.index.isocalendar().week == week)
                    & (_obj.index.isocalendar().day == day)
                ]

                # if there is a day
                day_length = arr[arr.shift() > 0].index.max() - arr[arr > 0].index.min()
                result[year][week][day] = {}

                if not pd.isna(day_length):

                    # build combinations for current day
                    shift_combinations = []
                    for r in range(
                        1, math.ceil(day_length / min(shifts)) + 1
                    ):  # just a bit more than one day_size
                        shift_combinations += [
                            x
                            for x in itertools.combinations_with_replacement(shifts, r)
                            if sum(sorted(x)[1:], datetime.timedelta(0, 0))
                            <= day_length
                        ]
                    shift_combinations = sorted(
                        shift_combinations,
                        key=lambda x: sum(x, datetime.timedelta(0, 0)),
                    )  # sort by sum of combination

                    combinations = []
                    [
                        combinations.append(shift_set)
                        for shift_set in shift_combinations
                        if sum(shift_set, datetime.timedelta(0, 0))
                        not in [
                            sum(shc, datetime.timedelta(0, 0)) for shc in combinations
                        ]
                    ]

                    # build the result layer by layer
                    for layer in range(int(arr.max())):

                        result[year][week][day][layer] = {}

                        layer_sets = np.array(
                            [
                                [a.index[0], a.index[-1],]  # start  # end
                                for a in np.split(
                                    arr, np.where(np.roll(arr, 1) == 0)[0]
                                )
                                if len(a) > 1
                            ]
                        )

                        layer_sets = _get_layer(arr, layer_sets, combinations)

                        layer_set_id = 0
                        for layer_set in layer_sets:
                            result[year][week][day][layer][layer_set_id] = {}

                            combo_starts = np.array(
                                [i for i in combinations[layer_set[3]]]
                            ).cumsum() - np.array(
                                [i for i in combinations[layer_set[3]]]
                            )
                            combo_ends = np.array(
                                [i for i in combinations[layer_set[3]]]
                            ).cumsum()

                            starts = arr.index[
                                [
                                    arr.index.get_loc(
                                        max(
                                            arr.index.min(),
                                            layer_set[0]
                                            + c
                                            - (
                                                (
                                                    (
                                                        (layer_set[4] - layer_set[2])
                                                        / freq
                                                    )
                                                    // 2
                                                )
                                                * freq
                                            ),
                                        )
                                    )
                                    for c in combo_starts
                                ]
                            ]
                            ends = arr.index[
                                [
                                    arr.index.get_loc(
                                        min(
                                            arr.index.max(),
                                            layer_set[0]
                                            + c
                                            - (
                                                (
                                                    (
                                                        (layer_set[4] - layer_set[2])
                                                        / freq
                                                    )
                                                    // 2
                                                )
                                                * freq
                                            ),
                                        )
                                    )
                                    for c in combo_ends
                                ]
                            ]

                            for i, s, e in zip(range(len(starts)), starts, ends):
                                result[year][week][day][layer][layer_set_id][i] = {}
                                result[year][week][day][layer][layer_set_id][i][
                                    "start"
                                ] = s - (adjust * freq)
                                result[year][week][day][layer][layer_set_id][i][
                                    "end"
                                ] = e - (adjust * freq)

                            layer_set_id += 1

                        # remove layer from arr
                        arr = arr.subtract(
                            pd.Series(index=arr.index, data=np.where(arr > 0, 1, 0)),
                            fill_value=0,
                        )

    frame = pd.DataFrame.from_dict(
        {
            (year, week, day, layer, layer_set_id, shift): result[year][week][day][
                layer
            ][layer_set_id][shift]
            for year in result.keys()
            for week in result[year].keys()
            for day in result[year][week].keys()
            for layer in result[year][week][day].keys()
            for layer_set_id in result[year][week][day][layer].keys()
            for shift in result[year][week][day][layer][layer_set_id].keys()
        },
        orient="index",
    )

    frame = frame.reset_index()
    frame.columns = ["year", "week", "day", "layer", "set", "shift", "start", "end"]

    return frame


def _combination_id(shift_length, combinations):
    return np.argmax(
        np.array([sum(shc, datetime.timedelta(0, 0)) for shc in combinations])
        >= shift_length
    )


def _get_layer(arr, layer, combinations):
    layer_duration = layer[:, 1] - layer[:, 0]
    layer = np.append(
        layer, layer_duration.reshape(layer.shape[0], 1), axis=1
    )  # add layer duration

    shift_combination_index = np.array(
        [_combination_id(x, combinations) for x in layer[:, 2]]
    )
    layer = np.append(
        layer, shift_combination_index.reshape(layer.shape[0], 1), axis=1
    )  # add shift_combination_index

    shift_duration = np.array(
        [
            sum(
                combinations[_combination_id(x, combinations)], datetime.timedelta(0, 0)
            )
            for x in layer[:, 2]
        ]
    )
    layer = np.append(
        layer, shift_duration.reshape(layer.shape[0], 1), axis=1
    )  # add shift duration

    layer = np.append(
        layer,
        layer[:, 0].reshape(layer.shape[0], 1)
        + shift_duration.reshape(layer.shape[0], 1),
        axis=1,
    )  # add shift start + shift duration

    layer = np.append(
        layer,
        layer[:, 0].reshape(layer.shape[0], 1)
        + np.array(
            [
                sum(
                    combinations[_combination_id(x, combinations)],
                    datetime.timedelta(0, 0),
                )
                for x in layer[:, 2]
            ]
        ).reshape(layer.shape[0], 1)
        + combinations[0],
        axis=1,
    )  # add shift start + shift duration + shift_combinations[0] duration

    if layer.shape[0] > 1:
        # a<b: start of next layer set < start of this layer + combination
        # c<d: end of next layer set < start of this layer + combination + smallest combination
        combine = np.array(
            [
                ([a < b, c < d])
                for a, b, c, d in zip(
                    layer[1:, 0], layer[:-1, 5], layer[1:, 1], layer[:-1, 6]
                )
            ]
        ).any(axis=1)

        # combine sets if applicable and get_layer
        combined = np.array(
            [(a[0], b[1]) for a, b, c in zip(layer[:-1, :], layer[1:, :], combine) if c]
        )
        if combined.shape[0] > 0:
            combined_sets = _get_layer(arr, combined, combinations)
            remaining_sets = np.delete(
                layer,
                [
                    (a, b)
                    for a, b, c in zip(
                        np.arange(0, combine.size + 1)[:-1],
                        np.arange(0, combine.size + 1)[1:],
                        combine,
                    )
                    if c
                ],
                axis=0,
            )

            # build final layer
            layer = np.append(combined_sets, remaining_sets, axis=0)
    return layer
