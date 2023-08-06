import numpy as np
import pandas as pd
import datetime


def reduce(_obj, *args, **kwargs):
    """
        Reduce the pandas object by grouping the index by value.
    
        Parameters
        ----------
        _obj: pandas Series or DataFrame

        Returns
        -------
        A pandas groupby object

        Example
        --------
        >>> index = pd.date_range('2022-01-01 12:00:00', periods=7, freq='15T')
        >>> data = [1., 2., 2., 3., 2., 2., 0.]]
        >>> series = pd.Series(index=index, data=data)
        >>> series
        2022-01-01 12:00:00    1.0
        2022-01-01 12:15:00    2.0
        2022-01-01 12:30:00    2.0
        2022-01-01 12:45:00    3.0
        2022-01-01 13:00:00    2.0
        2022-01-01 13:15:00    2.0
        2022-01-01 13:30:00    0.0
        dtype: float64
        
        Reduce the series
        >>> series._.reduce()
        2022-01-01 12:00:00    1.0
        2022-01-01 12:15:00    2.0
        2022-01-01 12:45:00    3.0
        2022-01-01 13:00:00    2.0
        2022-01-01 13:30:00    0.0
        dtype: float64

    """
    index = _obj.index[(_obj.values != _obj.shift().values)]
    data = _obj.groupby((_obj.values != _obj.shift().values).cumsum()).max().values

    if isinstance(_obj, pd.Series):
        return pd.Series(index=index, data=data, dtype=_obj.dtype, name=_obj.name)
    elif isinstance(_obj, pd.DataFrame):
        return pd.DataFrame(index=index, data=data, dtype=_obj.dtype)


def pivot(_obj, index=None, aggfunc="max", *args, **kwargs):
    """
    Reshape time-series data.

    Parameters
    ----------
    self: a Pandas Series object with DateTime index.
    rule: reshaping rule, default 'week'
        Indicates the new index level, 'year', 'week', 'day', 'hour',
        'minute' or 'second'. The lower levels are converted to columns.
    aggfunc: the Pandas.pivot_table aggfunc, default 'max'
    
    Returns
    -------
    a Pandas DataFrame object

    """
    levels = ["year", "week", "day", "hour", "minute", "second"]

    # get the gcd in seconds
    gcd = np.gcd.reduce(
        [
            int(x / np.timedelta64(1, "s"))
            for x in (_obj.index[1:] - _obj.index[:-1]).values
        ]
    )

    if gcd < 60:
        level = "second"
    elif gcd < 60 * 60:
        level = "minute"
    elif gcd < 60 * 60 * 24:
        level = "hour"
    elif gcd < 60 * 60 * 24 * 7:
        level = "day"
    else:
        level = "week"

    frame = pd.DataFrame(index=_obj.index, data={"values": _obj.values})
    frame.loc[:, ["year", "week", "day"]] = frame.index.isocalendar().values
    frame["hour"] = frame.index.hour
    frame["minute"] = frame.index.minute
    frame["second"] = frame.index.second
    result = frame.pivot_table(
        index=levels[: levels.index(index) + 1],
        columns=levels[levels.index(index) + 1 : levels.index(level) + 1],
        values="values",
        aggfunc=aggfunc,
    )

    return result

def stack(_obj, *args, **kwargs):
    """
    Stack pivoted time-series data.

    Parameters
    ----------
    self: a Pandas DataFrame object with MultiIndex.
    
    Returns
    -------
    a Pandas Series object with DatetimeIndex

    """
    series = _obj.stack(level=list(range(_obj.columns.nlevels)))
    series.index = pd.DatetimeIndex(series.index.map(lambda x: datetime.date.fromisocalendar(*x)))

    return series

class Reshape:
    def __init__(self, _obj, rule="w", level="m", aggfunc="max", **kwargs):
        self._obj = _obj
        self.rule = _get_rule(rule)
        self.level = _get_rule(level)
        self.levels = ["year", "week", "day", "hour", "minute", "second"]
        self.aggfunc = aggfunc
        self.kwargs = kwargs
        self.calculate()

    def calculate(self, **kwargs):

        if self.levels.index(self.rule) > self.levels.index(self.level):
            raise ValueError(
                "The 'rule' argument must be greater than or equal to the 'level' argument."
            )

        frame = pd.DataFrame(self._obj)
        frame.loc[:, ["year", "week", "day"]] = frame.index.isocalendar().values
        frame["hour"] = frame.index.hour
        frame["minute"] = frame.index.minute
        frame["second"] = frame.index.second
        self.result = frame.pivot_table(
            index=self.levels[: self.levels.index(self.rule) + 1],
            columns=self.levels[
                self.levels.index(self.rule) + 1 : self.levels.index(self.level) + 1
            ],
            values=self._obj.name,
            aggfunc=self.aggfunc,
        )

    def nsmallest(self, n=1):
        """
            Reshape the Timeline object and return a pandas Series for one period.
            The period is constructed as the percentile for every 'level' time slot
            over one 'rule' period.
        
            Parameters
            ----------
            self: Bluebelt Timeline object
            n: the n-th smallest value for every 'level' timeframe, default 1
            rule: reshaping rule, default 'week'
                Indicates the new index level, 'year', 'week', 'day', 'hour',
                'minute' or 'second'. The lower levels are converted to columns.
            level: the lowest level to return, default 'minute'
            
            Returns
            -------
            a Pandas DataFrame object

        """

        # yes, reshape to the lowest level and return a series
        result = Reshape(self._obj, rule=self.level).result.iloc[:, 0]

        # set groupby_levels
        groupby_levels = self.levels[
            self.levels.index(self.rule) + 1 : self.levels.index(self.level) + 1
        ]

        # and now groupby levels down to 'rule'
        result = (
            result.groupby(level=groupby_levels, group_keys=False)
            .nsmallest(n)
            .groupby(level=groupby_levels, group_keys=False)
            .nlargest(1)
        )

        return result

    def nlargest(self, n=1):
        """
            Reshape the Timeline object and return a pandas Series for one period.
            The period is constructed as the percentile for every 'level' time slot
            over one 'rule' period.
        
            Parameters
            ----------
            self: Bluebelt Timeline object
            n: the n-th largest value for every 'level' timeframe, default 1
            rule: reshaping rule, default 'week'
                Indicates the new index level, 'year', 'week', 'day', 'hour',
                'minute' or 'second'. The lower levels are converted to columns.
            level: the lowest level to return, default 'minute'
            
            Returns
            -------
            a Pandas DataFrame object

        """
        # yes, reshape to the lowest level and return a series
        result = Reshape(self._obj, rule=self.level).result.iloc[:, 0]

        # set groupby_levels
        groupby_levels = self.levels[
            self.levels.index(self.rule) + 1 : self.levels.index(self.level) + 1
        ]

        # and now groupby levels down to 'rule'
        result = (
            result.groupby(level=groupby_levels, group_keys=False)
            .nlargest(n)
            .groupby(level=groupby_levels, group_keys=False)
            .nsmallest(1)
        )

        return result

    def __repr__(self):
        return self.result.__repr__()


def _get_rule(rule):
    if isinstance(rule, str):
        rule = rule.replace(" ", "").lower()
        unit = rule.lstrip("0123456789")
        count = int(rule[0 : len(rule) - len(unit)]) if len(rule) > len(unit) else 1
        if unit in {"s", "sec", "second", "seconds"}:
            return "second"
        elif unit in {"m", "min", "minute", "minutes"}:
            return "minute"
        elif unit in {"h", "hr", "hrs", "hour", "hours"}:
            return "hour"
        elif unit in {"d", "day", "days"}:
            return "day"
        elif unit in {"w", "wk", "week", "weeks"}:
            return "week"
        elif unit in {"y", "yr", "year", "years"}:
            return "year"
        else:
            raise ValueError(
                "Value must be year-, week-, day-, hour-, minute- or second-like."
            )
    else:
        return rule
