import numpy as np
import pandas as pd
import datetime
import math

import bluebelt.data.shape

import bluebelt.helpers.check as check

import warnings

NoneType = type(None)


def resolution_methods(cls):
    def sum(self):
        result = self.grouped.sum(min_count=1)
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def mean(self):
        result = self.grouped.mean()
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def var(self):
        result = self.grouped.var()
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def std(self):
        result = self.grouped.std()
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def min(self):
        result = self.grouped.min()
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def max(self):
        result = self.grouped.max()
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def count(self):
        result = self.grouped.count()
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def value_range(self):
        result = self.grouped.apply(lambda x: x.max() - x.min())
        if isinstance(self, Flatten):
            result = result.reindex_like(self._obj, method="ffill")
        return result

    def nthsmallest(self, n=0, index="week", aggfunc="max"):

        pivot = bluebelt.data.shape.pivot(
            self.grouped.apply(aggfunc), index=index, aggfunc="max"
        )

        index = pivot.columns

        array = pivot.to_numpy()
        array = np.partition(array, n, axis=0)
        array = array[n : n + 1, :].flatten()
        return pd.Series(index=index, data=array)

    def nthlargest(self, n=0, aggfunc="max"):

        # not the smallest but the opposite
        n = array.shape[0] - (n + 1)

        pivot = bluebelt.data.shape.pivot(
            self.grouped.apply(aggfunc), index=index, aggfunc="max"
        )

        index = pivot.columns

        array = pivot.to_numpy()
        array = np.partition(array, n, axis=0)
        array = array[n : n + 1, :].flatten()
        return pd.Series(index=index, data=array)

    def subseries(self, count, size=1):
        """
        Count the number of times a list of 'count' items with size 'size' fit
        in each group.

        Parameters
        ----------
        self : GroupBy or Resampling object
        count: int
            The length of the sub-series.
        size: int
            The size of each element in the sub-series.

        Returns
        -------
        Series

        Example
        -------

        GroupBy or Resampling object: pd.Series([10, 8, 3, 3, 5])
        count: 3
        size: 1

        frame.blue.resample(rule=7).subseries(3, 1)
        >>> 9

        Every step subtracts (1, 1, 1, 0, 0), (1, 1, 0, 1, 0), (1, 1, 0, 0, 1),
        (1, 0, 0, 1, 1) or (0, 0, 1, 1, 1) from the group.

        step 0: (3, 3, 5, 8, 10)
        step 1: (3, 3, 4, 7, 9)
        step 2: (3, 3, 3, 6, 8)
        step 3: (2, 3, 3, 5, 7)
        step 4: (2, 2, 3, 4, 6)
        step 5: (2, 2, 2, 3, 5)
        step 6: (1, 2, 2, 2, 4)
        step 7: (1, 1, 1, 2, 3)
        step 8: (0, 1, 1, 1, 2)
        step 9: (0, 0, 0, 1, 1)
        """

        if not isinstance(count, int):
            raise ValueError("count must be an int")
        if not isinstance(size, (float, int)):
            raise ValueError("size must be float or int")
        # if isinstance(self._obj, pd.DataFrame):
        #     data = self._obj.sum(axis=1, numeric_only=True)

        def _subseries_count(series, count=3, size=1):
            # helper for resample.subseries
            series = pd.Series(series) / size
            result = series.sum() * count
            for i in range(count, 0, -1):
                result = np.minimum(
                    result,
                    math.floor(series.nsmallest(len(series) - count + i).sum() / i),
                )
            return result

        if isinstance(self._obj, pd.Series):
            result = pd.Series(
                index=self.grouped.groups.keys(),
                data=self.grouped.apply(
                    lambda x: _subseries_count(series=x, count=count, size=size)
                ).values,
                name=f"subseries {str(count)} of {str(size)}",
            )
        elif isinstance(self._obj, pd.DataFrame):
            result = pd.DataFrame(
                index=self.grouped.groups.keys(),
                data=self.grouped.apply(
                    lambda x: _subseries_count(series=x, count=count, size=size),
                ).values,
                columns=self._obj.columns,
            )

        return result

    def diff_quantity(self, shift=1, skip_na=True, skip_zero=True):
        # if this week > last week: this week - last week / this week
        # if this week < last week: last week - this week / last week

        if isinstance(self._obj, pd.DataFrame):
            data = self._obj.sum(
                axis=1, min_count=1
            )  # min_count=1 prevents np.nan values to become zeros
        else:
            data = self._obj

        # resample the data and transpose into a DataFrame with weekdays as columns
        data = data.resample(rule=self.rule, origin=self.origin, **self.kwargs)
        data = data.apply(
            lambda x: pd.DataFrame(
                index=x.index.isocalendar().day, data=x.values,
            ).transpose()
        )

        # drop the extra index level that was created in the transpose
        data = data.droplevel(-1)

        # get the difference, but only for days where both weeks have a proper value
        if skip_na and skip_zero:
            result = (
                data[(data.shift(shift).notna()) & (data.shift(shift) != 0)]
                - data.shift(shift)[(data.notna()) & (data != 0)]
            ).sum(axis=1).abs() / np.maximum(
                data[(data.shift(shift).notna()) & (data.shift(shift) != 0)].sum(
                    axis=1
                ),
                data.shift(shift)[(data.notna()) & (data != 0)].sum(axis=1),
            )
        elif skip_na:
            result = (
                data[data.shift(shift).notna()] - data.shift(shift)[data.notna()]
            ).sum(axis=1).abs() / np.maximum(
                data[data.shift(shift).notna()].sum(axis=1),
                data.shift(shift)[data.notna()].sum(axis=1),
            )
        elif skip_zero:
            result = (data[data.shift(shift) != 0] - data.shift(shift)[data != 0]).sum(
                axis=1
            ).abs() / np.maximum(
                data[data.shift(shift) != 0].sum(axis=1),
                data.shift(shift)[data != 0].sum(axis=1),
            )
        else:
            result = (data - data.shift(shift)).sum(axis=1).abs() / np.maximum(
                data.sum(axis=1), data.shift(shift).sum(axis=1)
            )

        return result

    def diff_distribution(self, shift=1, skip_na=True, skip_zero=True):
        # only works with resample('1w') or equivalent
        if self.rule != datetime.timedelta(days=7):
            raise ValueError(
                f"The object must be resampled to weekly data not {self.rule}"
            )

        # if a DataFrame is passed then sum the columns
        if isinstance(self._obj, pd.DataFrame):
            data = self._obj.sum(axis=1, numeric_only=True)
        else:
            data = self._obj

        # resample the data and transpose into a DataFrame with weekdays as columns
        data = data.resample(rule=self.rule, origin=self.origin, **self.kwargs)
        data = data.apply(
            lambda x: pd.DataFrame(
                index=x.index.isocalendar().day, data=x.values,
            ).transpose()
        )

        # drop the extra index level that was created in the transpose
        data = data.droplevel(-1)

        # get diff_quantity to calculate the relative difference
        if skip_na and skip_zero:
            diff = (
                (
                    data[(data.shift(shift).notna()) & (data.shift(shift) != 0)]
                    - data.shift(shift)[(data.notna()) & (data != 0)].multiply(
                        data[
                            (data.shift(shift).notna()) & (data.shift(shift) != 0)
                        ].sum(axis=1)
                        / data.shift(shift)[(data.notna()) & (data != 0)].sum(axis=1),
                        axis=0,
                    )
                )
                .abs()
                .sum(axis=1, min_count=1)
            )
        elif skip_na:
            diff = (
                (
                    data[data.shift(shift).notna()]
                    - data.shift(shift)[data.notna()].multiply(
                        data[data.shift(shift).notna()].sum(axis=1)
                        / data.shift(shift)[data.notna()].sum(axis=1),
                        axis=0,
                    )
                )
                .abs()
                .sum(axis=1, min_count=1)
            )
        elif skip_zero:
            diff = (
                (
                    data[data.shift(shift) != 0]
                    - data.shift(shift)[data != 0].multiply(
                        data[data.shift(shift) != 0].sum(axis=1)
                        / data.shift(shift)[data != 0].sum(axis=1),
                        axis=0,
                    )
                )
                .abs()
                .sum(axis=1, min_count=1)
            )
        else:
            diff = (
                (
                    data
                    - data.shift(shift).multiply(
                        data.sum(axis=1) / data.shift(shift).sum(axis=1), axis=0,
                    )
                )
                .abs()
                .sum(axis=1, min_count=1)
            )

        # build result
        result = pd.Series(
            diff / (data.sum(axis=1, min_count=1) * 2), name="distribution",
        )

        return result

    def diff_skills(self, shift=1, skip_na=True, skip_zero=True):

        """
        Calculate the difference in skills distribution from week to week in
        from a resampled DataFrame.

        Parameters
        ----------
        self : GroupBy or Resampling object

        Returns
        -------
        Series

        Example
        -------
        index = pd.date_range(start='2022-03-07 00:00:00', periods=21)
        data = {'skill 1': [20,20,10,15,10,10,10,
                            20,20,10,10,10,10,10,
                            20,20,10,10,10,10,10,],
                'skill 2': [20,10,20,5,10,10,10,
                            20,20,10,10,10,10,10,
                            20,10,20,10,10,10,10,],
                }
        frame = pd.DataFrame(index=index, data=data)

        >>> frame.blue.resample(rule=7).diff_skills()

        2022-03-07         NaN
        2022-03-14    0.027778
        2022-03-21    0.000000
        Name: skills, dtype: float64
        """

        # only works with resample('1w') or equivalent
        if self.rule != datetime.timedelta(days=7):
            raise ValueError(
                f"The object must be resampled to weekly data not {self.rule}"
            )

        # if the object is a Series return Series of zeros.
        if isinstance(self._obj, pd.Series):
            return pd.Series(
                index=self.grouped.sum().index,
                data=np.zeros(self.grouped.sum().size),
                name="skills",
            )

        # resample the data and transpose into a DataFrame with weekdays as columns
        data = self.grouped.apply(
            lambda x: pd.DataFrame(
                index=x.index.isocalendar().day, data=x.values, columns=x.columns,
            ).transpose()
        )

        # build a filter for the dataframe for weekdays with value zero or np.nan
        summed = data.groupby(level=0).apply(pd.DataFrame.sum, skipna=True)

        filt_index = pd.MultiIndex.from_product([summed.index, self._obj.columns])
        filt_data = np.repeat(summed.values, repeats=self._obj.shape[1], axis=0)

        if skip_na and skip_zero:
            filt_data = (filt_data != 0) & (np.logical_not(np.isnan(filt_data)))
        elif skip_na:
            filt_data = np.logical_not(np.isnan(filt_data))
        elif skip_zero:
            filt_data = filt_data != 0
        else:
            filt_data = np.full(filt_data.shape, True)

        filt = pd.DataFrame(index=filt_index, data=filt_data, columns=summed.columns,)

        # get diff_quantity to calculate the relative difference
        if skip_na and skip_zero:
            diff_quantity = summed[
                (summed.shift(shift).notna()) & (summed.shift(shift) != 0)
            ].sum(axis=1) / summed.shift(shift)[(summed.notna()) & (summed != 0)].sum(
                axis=1
            )
        elif skip_na:
            diff_quantity = summed[summed.shift(shift).notna()].sum(
                axis=1
            ) / summed.shift(shift)[summed.notna()].sum(axis=1)
        elif skip_zero:
            diff_quantity = summed[summed.shift(shift) != 0].sum(axis=1) / summed.shift(
                shift
            )[summed != 0].sum(axis=1)
        else:
            diff_quantity = summed.sum(axis=1) / summed.shift(shift).sum(axis=1)

        # calculate diff_skills

        # filter the data with shifted filter and the shifted data with the unshifted filter
        # remember that the shift is equal to the number of skills (self._obj.shape[1])
        # sum the data for the weekdays
        # unstack the skills => the result is grouped data with skills as columns

        diff = (
            # the data with shifted filter minus the shifted data with filter
            (
                data[filt.shift(self._obj.shape[1] * shift)]
                .sum(axis=1)
                .unstack(level=1)
                - data.shift(self._obj.shape[1] * shift)[filt]
                .sum(axis=1)
                .unstack(level=1)
                .multiply(diff_quantity, axis=0)
            )
            .abs()
            .sum(axis=1, min_count=1)
        )

        # get the difference relative to the sum of the row with the shifted filter applied
        result = pd.Series(
            diff
            / (
                data[filt.shift(self._obj.shape[1] * shift)]
                .sum(axis=1)
                .unstack(level=1)
                .sum(axis=1, min_count=1)
                * 2
            ),
            name="skills",
        )

        return result

    setattr(cls, "sum", sum)
    setattr(cls, "mean", mean)
    setattr(cls, "var", var)
    setattr(cls, "std", std)
    setattr(cls, "min", min)
    setattr(cls, "max", max)
    setattr(cls, "count", count)
    setattr(cls, "value_range", value_range)
    setattr(cls, "nthsmallest", nthsmallest)
    setattr(cls, "nthlargest", nthlargest)
    setattr(cls, "subseries", subseries)
    setattr(cls, "diff_quantity", diff_quantity)
    setattr(cls, "diff_distribution", diff_distribution)
    setattr(cls, "diff_skills", diff_skills)
    return cls


@resolution_methods
class Resample:
    """
    Resample time-series data.
    The object must have a DatetimeIndex

    Parameters
    ----------
    self: Series or DataFrame
    rule: DateOffset, Timedelta or str, default 'week'
        The offset string or object representing target conversion.
        e.g. '1w', 'week', '4d', '4 days'
    ffill: Forward fill data if applicable, default None
        If 'rule' is smaller than the greatest step in the index values of self
        the NaN values will be forward filled if True. Does raise a warning to
        point out this behaviour.

    kwargs: other pandas.Series.resample keywords

    Returns
    -------
    pandas.core.Resampler

    Methods
    -------
    sum: Calculate the sum of all the values in each group.
    mean: Calculate the mean of all the values in each group.
    var: Calculate the variance of all the values in each group.
    std: Calculate the standard deviation of all the values in each group.
    min: Calculate the minimum value of all the values in each group.
    max: Calculate the maximum value of all the values in each group.
    count: Calculate the count of all the values in each group.
    value_range: Calculate the value range of all the values in each group.
    subsize: Calculate the count of subgroups with a size that fit in each
        group.
    diff_quantity: Calculate the difference of the sum of all values
        in adjecent groups of the resampled DataFrame.
    diff_distribution: Calculate the difference in weekday distribution
        from week to week in from a resampled DataFrame. The rule for
        resampling must be '1w' or equivalent
    diff_skills: Calculate the difference in skills distribution from week
        to week in from a resampled DataFrame. The rule for resampling must
        be '1w' or equivalent.

    """

    def __init__(self, _obj, rule, ffill=None, **kwargs):
        self._obj = _obj
        self.rule = _get_rule(rule)
        self.ffill = ffill
        self.gcd = np.gcd.reduce(
            [
                int(x / np.timedelta64(1, "ns"))
                for x in (_obj.index[1:] - _obj.index[:-1]).values
            ]
        )
        self.origin = _get_origin(_obj, self.rule)
        self.kwargs = kwargs
        self.calculate()

    def calculate(self, **kwargs):

        if isinstance(self.ffill, NoneType):
            # consider timeline to have closed attribute
            warnings.warn(
                f"\n\n"
                + f"The resample rule ({pd.Timedelta(self.rule)}) is smaller than the "
                + f"greatest step in the series index values ({(self._obj.index[1:] - self._obj.index[:-1]).max()}). "
                + f"This results in NaN values in the resampled series."
                + f"\nTo prevent this the gaps in the data are forward filled. To prevent this behaviour set 'ffill=False'.\n "
                + f"\nSilence this warning by setting 'ffill=True'.\n ",
                Warning,
            )

            self.ffill = True

        # check if the rule < greatest diff
        if (
            pd.Timedelta(self.rule) < (self._obj.index[1:] - self._obj.index[:-1]).max()
            and self.ffill
        ):

            self.grouped = (
                self._obj.resample(f"{self.gcd}ns")
                .ffill()
                .resample(rule=self.rule, origin=self.origin, **self.kwargs)
            )

        else:
            self.grouped = self._obj.resample(
                rule=self.rule, origin=self.origin, **self.kwargs
            )

    def __repr__(self):
        return self.grouped.__repr__()

    def apply(self, func, *args, **kwargs):
        return self.grouped.apply(func, *args, **kwargs)


class Flatten(Resample):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr):
        return super().__getattr__(attr).reindex_like(self._obj, method="ffill")

    # result = result.reindex_like(self._obj, method="ffill")


def _get_origin(_obj, rule):
    if (rule / datetime.timedelta(days=7)).is_integer():
        days = int(
            ((_obj.index.isocalendar().week[0] - 1) * 7) + _obj.index[0].weekday()
        )
        return _obj.index[0] - datetime.timedelta(days=days)
    elif (rule / datetime.timedelta(days=1)).is_integer():
        days = int(_obj.index[0].weekday())
        return _obj.index[0] - datetime.timedelta(days=days)
    else:
        return "start_day"


def _get_rule(rule):
    if isinstance(rule, str):
        rule = rule.replace(" ", "").lower()
        unit = rule.lstrip("0123456789")
        count = int(rule[0 : len(rule) - len(unit)]) if len(rule) > len(unit) else 1
        if unit in {"μs", "microsecond", "microseconds"}:
            return datetime.timedelta(microseconds=count)
        if unit in {"ms", "millisecond", "milliseconds"}:
            return datetime.timedelta(milliseconds=count)
        if unit in {"s", "sec", "second", "seconds"}:
            return datetime.timedelta(seconds=count)
        if unit in {"m", "min", "minute", "minutes"}:
            return datetime.timedelta(minutes=count)
        if unit in {"h", "hr", "hrs", "hour", "hours"}:
            return datetime.timedelta(hours=count)
        if unit in {"d", "day", "days"}:
            return datetime.timedelta(days=count)
        if unit in {"w", "wk", "week", "weeks"}:
            return datetime.timedelta(weeks=count)
    elif isinstance(rule, int):
        return datetime.timedelta(days=rule)
    else:
        return rule
