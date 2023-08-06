import pandas as pd
import numpy as np

import bluebelt.data.resolution
import bluebelt.data.shape
import bluebelt.data.timeline

import bluebelt.helpers.check as check
import bluebelt.helpers.convert
from bluebelt.helpers.io import to_pickle

from bluebelt.helpers.decorators.docstring import docstring

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import seaborn as sns

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import bluebelt.helpers.matplotlib2plotly as m2p

import copy
import datetime
import os


class Timeline:
    def __init__(
        self,
        other,
        start=None,
        end=None,
        value=None,
        name=None,
        dtype=None,
        *args,
        **kwargs,
    ):

        if isinstance(other, pd.Series):
            if isinstance(other.index, pd.MultiIndex) and all(
                [x in other.index.names for x in ["day", "hour", "minute"]]
            ):
                other.index = other.index.map(
                    lambda x: datetime.datetime.combine(
                        datetime.date.fromisocalendar(1973, 16, x[0]),
                        datetime.time(x[1], x[2]),
                    )
                )
                other.index.freq = min(other.index[1:] - other.index[:-1])

            elif not isinstance(other.index, pd.DatetimeIndex):
                raise ValueError(
                    f"Index must be a DatetimeIndex or MultiIndex with 'day', 'hour' and 'minute' not {type(other.index).__name__}."
                )
            self._obj = other

        elif isinstance(other, pd.DataFrame):
            check.is_str(start, end)
            check.is_str_or_none(value)

            # clean the dataframe
            other = other[other[start] != other[end]]  # remove rows with start == end
            other = other[
                ~(other[start].isna() | other[end].isna())
            ]  # remove NaT values

            # set new index
            index = (
                pd.Index(other[start].values)
                .union(pd.Index(other[end].values))
                .drop_duplicates(keep="first")
            )

            # build input series
            if value:
                series = other.groupby([start, end])[value].sum().rename("value")
            else:
                series = other.groupby([start, end])[start].count().rename("value")

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
                        ((index.values >= key[0]) & (index.values < key[1])).astype(
                            float
                        ),
                        value,
                    ),
                )

            result = pd.Series(
                index=index, data=array, name=name, dtype=(dtype or array.dtype)
            )

            # remove duplicate indices
            result = result[~result.index.duplicated(keep="first")]

            self._obj = result

    def __repr__(self):
        print("Timeline")
        return self._obj.__repr__()

    def __getattr__(self, attr):
        return self._obj.__getattr__(attr)

    def __add__(self, other):
        index = self._obj.index.union(other._obj.index)
        t1 = self._obj.reindex(index).ffill().fillna(0)
        t2 = other._obj.reindex(index).ffill().fillna(0)
        return Timeline(t1.add(t2))

    def __sub__(self, other):
        index = self._obj.index.union(other._obj.index)
        t1 = self._obj.reindex(index).ffill().fillna(0)
        t2 = other._obj.reindex(index).ffill().fillna(0)

        result = t1.subtract(t2)
        return Timeline(result.where(result > 0, 0))

    def to_pickle(self, path):
        to_pickle(self, path)

    @docstring(bluebelt.data.shape.reduce)
    def reduce(self, *args, **kwargs):
        return Timeline(bluebelt.data.shape.reduce(self._obj, **kwargs))

    @docstring(bluebelt.data.resolution.Resample)
    def resample(self, rule="15m", ffill=True, aggfunc="max", *args, **kwargs):
        result = bluebelt.data.resolution.Resample(self._obj, rule, ffill=ffill)
        return Timeline(getattr(result, aggfunc)(*args, **kwargs))

    @docstring(bluebelt.data.shape.pivot)
    def pivot(self, index="week", aggfunc="max", **kwargs):
        check.has_datetimeindex(self._obj)
        return bluebelt.data.shape.pivot(
            self._obj, index=index, aggfunc=aggfunc, **kwargs
        )

    @docstring(bluebelt.data.projection.project)
    def project(self, year=None, adjust_holidays=True):
        return Timeline(
            bluebelt.data.projection.project(
                self._obj, year=year, adjust_holidays=adjust_holidays
            )
        )

    def reshape(self, rule="week", level="minute", aggfunc="max"):
        """
            Reshape the Timeline object.
        
            Parameters
            ----------
            self: Bluebelt Timeline object
            rule: reshaping rule, default 'week'
                Indicates the new index level, 'year', 'week', 'day', 'hour',
                'minute' or 'second'. The lower levels are converted to columns.
            level: the lowest level to return, default 'minute'
            aggfunc: the Pandas.pivot_table aggfunc, default 'max'
            
            Returns
            -------
            a Pandas DataFrame object

        """
        name = self._obj.name
        levels = ["year", "week", "day", "hour", "minute", "second"]

        if not (rule in levels and level in levels):
            raise ValueError(
                "Both rule and level should be 'year', 'week', 'day', 'hour', 'minute' or 'second'"
            )

        # avoid trouble if the level has a lower index than rule
        level = level if levels.index(rule) < levels.index(level) else rule

        frame = pd.DataFrame(self._obj)
        frame.loc[:, ["year", "week", "day"]] = frame.index.isocalendar()
        frame["hour"] = frame.index.hour
        frame["minute"] = frame.index.minute
        frame["second"] = frame.index.second
        return frame.pivot_table(
            index=levels[: levels.index(rule) + 1],
            columns=levels[levels.index(rule) + 1 : levels.index(level) + 1],
            values=name,
            aggfunc=aggfunc,
        )

    def percentile(self, percentile=0.1, how="smallest", rule="week", level="minute"):
        """
            Reshape the Timeline object and return a pandas Series for one period.
            The period is constructed as the percentile for every 'level' time slot
            over one 'rule' period.
        
            Parameters
            ----------
            self: Bluebelt Timeline object
            percentile: the percentile to calculate, default 0.1
            how: calculate the percentile as 'smallest' or 'largest', default 'smallest'
            rule: reshaping rule, default 'week'
                Indicates the new index level, 'year', 'week', 'day', 'hour',
                'minute' or 'second'. The lower levels are converted to columns.
            level: the lowest level to return, default 'minute'
            
            Returns
            -------
            a Pandas DataFrame object

        """
        levels = ["year", "week", "day", "hour", "minute", "second"]

        # avoid trouble if the level has a lower index than rule
        level = (
            level
            if levels.index(rule) < levels.index(level)
            else levels[levels.index(rule) + 1]
        )

        # pivot to the lowest level and return a series
        result = self.pivot(index=level).max(axis=1)

        # get n from percentile
        n = np.round(
            result.groupby(level=levels[: levels.index(rule) + 1]).ngroups * percentile
        ).astype(int)

        # set groupby_levels
        groupby_levels = levels[levels.index(rule) + 1 : levels.index(level) + 1]

        # and now groupby levels down to 'rule'
        if how == "largest":
            result = (
                result.groupby(level=groupby_levels, group_keys=False)
                .nlargest(n)
                .groupby(level=groupby_levels, group_keys=False)
                .nsmallest(1)
            )
        elif how == "smallest":
            result = (
                result.groupby(level=groupby_levels, group_keys=False)
                .nsmallest(n)
                .groupby(level=groupby_levels, group_keys=False)
                .nlargest(1)
            )
        else:
            raise ValueError(
                f"parameter 'how' must be 'smallest' or 'largest', not {how}."
            )

        return result

    def nthsmallest(self, n=1, rule="week", level="minute"):
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
        levels = ["year", "week", "day", "hour", "minute", "second"]

        # avoid trouble if the level has a lower index than rule
        level = (
            level
            if levels.index(rule) < levels.index(level)
            else levels[levels.index(rule) + 1]
        )

        # pivot to the lowest level and return a series
        result = self.pivot(index=level).max(axis=1)

        # set groupby_levels
        groupby_levels = levels[levels.index(rule) + 1 : levels.index(level) + 1]

        # and now groupby levels down to 'rule'
        result = (
            result.groupby(level=groupby_levels, group_keys=False)
            .nsmallest(n)
            .groupby(level=groupby_levels, group_keys=False)
            .max()
        )

        return result

    nsmallest = nthsmallest

    def nthlargest(self, n=1, rule="week", level="minute"):
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
        levels = ["year", "week", "day", "hour", "minute", "second"]

        # avoid trouble if the level has a lower index than rule
        level = (
            level
            if levels.index(rule) < levels.index(level)
            else levels[levels.index(rule) + 1]
        )

        # pivot to the lowest level and return a series
        result = self.pivot(index=level).max(axis=1)

        # set groupby_levels
        groupby_levels = levels[levels.index(rule) + 1 : levels.index(level) + 1]

        # and now groupby levels down to 'rule'
        result = (
            result.groupby(level=groupby_levels, group_keys=False)
            .nlargest(n)
            .groupby(level=groupby_levels, group_keys=False)
            .min()
        )

        return result

    nlargest = nthlargest

    def filter(self, year=None, week=None, day=None, *args, **kwargs):

        _obj = copy.copy(self._obj)

        if year and isinstance(year, str):
            year = bluebelt.helpers.convert.str_to_list_of_int(year)
        if year and isinstance(year, int):
            _obj = _obj[_obj.index.isocalendar().year == year]
        elif year and isinstance(year, (list, tuple)):
            _obj = _obj[_obj.index.isocalendar().year.isin(year)]

        if week and isinstance(week, str):
            week = bluebelt.helpers.convert.str_to_list_of_int(week)
        if week and isinstance(week, int):
            _obj = _obj[_obj.index.isocalendar().week == week]
        elif week and isinstance(week, (list, tuple)):
            _obj = _obj[_obj.index.isocalendar().week.isin(week)]

        if day and isinstance(day, str):
            day = bluebelt.helpers.convert.str_to_list_of_int(day)
        if day and isinstance(day, int):
            _obj = _obj[_obj.index.isocalendar().day == day]
        elif day and isinstance(day, (list, tuple)):
            _obj = _obj[_obj.index.isocalendar().day.isin(day)]

        return Timeline(_obj)

    def standard_week(
        self,
        how="nthsmallest",
        n=1,
        level="minute",
        year=None,
        week=None,
        day=None,
        *args,
        **kwargs,
    ):

        if how in ["nsmallest", "nthsmallest"]:
            _sw = self.nthsmallest(n=n, rule="week", level=level).to_dict()
        elif how in ["nlargest", "nthlargest"]:
            _sw = self.nthlargest(n=n, rule="week", level=level).to_dict()
        else:
            raise ValueError(
                f"'how' must be 'nthsmallest' or 'nthlargest', not '{how}'."
            )

        return Timeline(
            self.filter(year=year, week=week, day=day, *args, **kwargs)
            ._obj.index.to_series()
            .apply(lambda x: _sw.get((x.isocalendar().weekday, x.hour, x.minute)))
        )

    @docstring(bluebelt.data.timeline.get_shifts)
    def get_shifts(
        self,
        shifts=None,
        adjust_midnight=0,
        freq=None,
        *args,
        **kwargs,
    ):
        return TimelineShifts(
            self._obj,
            shifts=shifts,
            adjust_midnight=adjust_midnight,
            freq=freq,
            *args,
            **kwargs,
        )


class TimelineShifts:
    def __init__(
        self,
        _obj,
        shifts=None,
        adjust_midnight=0,
        freq=None,
        *args,
        **kwargs,
    ):
        self._obj = _obj
        self.shifts = shifts
        self.adjust_midnight = adjust_midnight

        # filter _obj
        if freq is None and _obj.index.freq is None:
            freq = self._get_freq()
        elif freq is None:
            freq = pd.Timedelta(_obj.index.freq.freqstr)

        self._obj = _obj
        self.frame = bluebelt.data.timeline.get_shifts(
            self._obj,
            shifts=shifts,
            adjust_midnight=adjust_midnight,
            freq=freq,
            *args,
            **kwargs,
        )

    def __repr__(self):
        return self.frame.__repr__()

    def _repr_html_(self):
        return self.frame._repr_html_()

    def _get_freq(self):

        gcd = np.gcd.reduce(
            [
                int(x / np.timedelta64(1, "ns"))
                for x in (self._obj.index[1:] - self._obj.index[:-1]).values
            ]
        )
        return pd.Timedelta(f"{gcd}ns")

    def to_pickle(self, path):
        to_pickle(self, path)

    def plot(
        self,
        xlim=(None, None),
        ylim=(None, None),
        max_xticks=None,
        format_xticks=None,
        format_yticks=None,
        title=None,
        xlabel=None,
        ylabel=None,
        palette=None,
        legend=True,
        path=None,
        **kwargs,
    ):

        palette = palette or bluebelt.style("colors")[1:]

        if bluebelt.config("plotting") == "matplotlib":

            colors = {
                s: c for s, c in zip(self.shifts, sns.color_palette(palette).as_hex())
            }

            # prepare figure
            fig, ax = plt.subplots(nrows=1, ncols=1, **kwargs)

            ax.plot(self._obj, **bluebelt.style(f"line"))

            for i, row in self.frame.iterrows():
                ax.add_patch(
                    Rectangle(
                        (row["start"], row["layer"]),
                        row["end"] - row["start"],
                        1,
                        color=colors.get(
                            (row["end"] - row["start"]) / datetime.timedelta(minutes=60)
                        ),
                        lw=0,
                    )
                )

            # limit axis
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

            # set ticks
            bluebelt.helpers.ticks.year_week(self._obj, ax=ax, max_xticks=max_xticks)

            # format ticks
            if format_xticks:
                ax.set_xticks(ax.get_xticks())
                ax.set_xticklabels([f"{x:{format_xticks}}" for x in ax.get_xticks()])
            if format_yticks:
                ax.set_yticks(ax.get_yticks())
                ax.set_yticklabels([f"{y:{format_yticks}}" for y in ax.get_yticks()])

            # labels
            if title:
                ax.set_title(title)
            if xlabel:
                ax.set_xlabel(xlabel)
            if ylabel:
                ax.set_ylabel(ylabel)

            # legend
            if legend:
                legend_elements = [
                    Patch(facecolor=c, label=f"{s} hour shift")
                    for s, c in zip(self.shifts, sns.color_palette(palette).as_hex())
                ]
                ax.legend(handles=legend_elements, loc="best")
            elif ax.get_legend() is not None:
                ax.get_legend().set_visible(False)

            plt.tight_layout()

            # file
            if path:
                if len(os.path.dirname(path)) > 0 and not os.path.exists(
                    os.path.dirname(path)
                ):
                    os.makedirs(os.path.dirname(path))
                plt.savefig(path)
                plt.close()
            else:
                plt.close()
                return fig

        elif bluebelt.config("plotting") == "plotly":

            layout = go.Layout(
                m2p.layout(
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    xlim=xlim,
                    ylim=ylim,
                    format_xticks=format_xticks,
                    format_yticks=format_yticks,
                    legend=legend,
                    **kwargs,
                )
            )

            data = [
                dict(
                    type="scatter",
                    mode="lines",
                    x=np.array(
                        [
                            [row["start"], row["end"], row["end"], row["start"], None]
                            for i, row in self.frame.iterrows()
                            if (row["end"] - row["start"]) / pd.Timedelta("1h") == shift
                        ]
                    ).flatten()[:-1],
                    y=np.array(
                        [
                            [
                                row["layer"],
                                row["layer"],
                                row["layer"] + 1,
                                row["layer"] + 1,
                                None,
                            ]
                            for i, row in self.frame.iterrows()
                            if (row["end"] - row["start"]) / pd.Timedelta("1h") == shift
                        ]
                    ).flatten()[:-1],
                    name=f"{shift} hour shift",
                    line=dict(width=0),
                    fill="toself",
                    fillcolor=m2p.to_rgba(
                        bluebelt.style("colors")[self.shifts.index(shift) + 1], 1
                    ),
                    opacity=1,
                )
                for shift in self.shifts
            ] + [
                dict(
                    type="scatter",
                    mode="lines",
                    x=self._obj.index,
                    y=self._obj.values,
                    name=self._obj.name or "timeline",
                    line=dict(
                        color=bluebelt.style("colors")[0],
                        width=bluebelt.style("line.linewidth"),
                        dash="dot",
                    ),
                    opacity=1,
                )
            ]

            fig = go.Figure(data=data, layout=layout)

            return fig

