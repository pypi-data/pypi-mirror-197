import numpy as np
import pandas as pd

import bluebelt.helpers.check as check
import bluebelt.core.series

import bluebelt.analysis.forecast

import bluebelt.statistics.hypothesis_testing
import bluebelt.statistics.basic

from bluebelt.helpers.decorators.docstring import docstring


@pd.api.extensions.register_dataframe_accessor("_")
@pd.api.extensions.register_dataframe_accessor("blue")
class DataFrameToolkit:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self.stats = self.stats(self._obj)

        # copy Series functions
        self.weekend = bluebelt.core.series.SeriesToolkit(self._obj).weekend
        self.not_weekend = bluebelt.core.series.SeriesToolkit(self._obj).not_weekend
        self.weekdays = bluebelt.core.series.SeriesToolkit(self._obj).weekdays
        self.holiday = bluebelt.core.series.SeriesToolkit(self._obj).holiday
        self.holidays = bluebelt.core.series.SeriesToolkit(self._obj).holidays
        self.not_holiday = bluebelt.core.series.SeriesToolkit(self._obj).not_holiday
        self.not_holidays = bluebelt.core.series.SeriesToolkit(self._obj).not_holidays
        self.workdays = bluebelt.core.series.SeriesToolkit(self._obj).workdays

        self.resample = bluebelt.core.series.SeriesToolkit(self._obj).resample
        self.project = bluebelt.core.series.SeriesToolkit(self._obj).project

        self.line = bluebelt.core.series.SeriesToolkit(self._obj).line
        self.bar = bluebelt.core.series.SeriesToolkit(self._obj).bar
        self.area = bluebelt.core.series.SeriesToolkit(self._obj).area
        self.hist = bluebelt.core.series.SeriesToolkit(self._obj).hist
        self.dist = bluebelt.core.series.SeriesToolkit(self._obj).dist
        self.histogram = bluebelt.core.series.SeriesToolkit(self._obj).hist
        self.box = bluebelt.core.series.SeriesToolkit(self._obj).box
        self.boxplot = bluebelt.core.series.SeriesToolkit(self._obj).box

        # copy Series classes
        self.planning = bluebelt.core.series.SeriesToolkit(self._obj).planning
        self.forecast = bluebelt.core.series.SeriesToolkit(self._obj).forecast

    def fill_na(self):
        """
        Fill all missing values of a pandas DataFrame with the
        interpolated values of the previous and next weeks weekday.

        Parameters
        ----------
        self: DataFrame

        Returns
        -------
        pandas.DataFrame
        """
        result = pd.DataFrame(index=self._obj.index)

        for column in self._obj:
            result[column] = bluebelt.core.series.SeriesToolkit(
                self._obj[column]
            ).fill_na()

        return result

    @docstring(bluebelt.data.shape.stack)
    def stack(self, *args, **kwargs):
        return bluebelt.data.shape.stack(self._obj, *args, **kwargs)

    def project(self, year=None, adjust_holidays=True):
        return bluebelt.data.projection.project(
            self._obj, year=year, adjust_holidays=adjust_holidays
        )

    def subset(self, inverse=False, **kwargs):
        """
        Create a subset based on the pandas.Dataframe column values.

        Parameters
        ----------
        frame: pandas.DataFrame
        inverse: bool, default False
            inverse the result
        kwargs: str=*
            columns names as arguments and values as values or a list of values
            any space in the column name can be replaced with an underscore (_)

        Returns
        -------
        Subset


        Example
        -------

        df
            | column_1  | column_2  | column_3  |
        -----------------------------------------
        0   | a         | a         | a         |
        1   | b         | a         | b         |
        2   | a         | b         | c         |
        3   | b         | b         | a         |
        4   | a         | c         | b         |
        5   | b         | c         | c         |
        6   | a         | a         | a         |
        7   | b         | a         | b         |
        8   | a         | b         | c         |
        9   | b         | b         | a         |

        >> subset = bluebelt.data.subsets.Subset(frame, column_1="a", column_2=["a", "b"])
        >> subset

            | column_1  | column_2  | column_3  |
        -----------------------------------------
        0   | a         | a         | a         |
        2   | a         | b         | c         |
        6   | a         | a         | a         |
        8   | a         | b         | c         |
        """

        # build filters
        filters = {}
        for col in kwargs:
            if col in self._obj.columns:
                values = (
                    kwargs.get(col)
                    if isinstance(kwargs.get(col), list)
                    else [kwargs.get(col)]
                )
                for value in values:
                    if value not in self._obj[col].values:
                        raise ValueError(f"{value} is not in {col}")
                filters[col] = values
            elif col.replace("_", " ") in self._obj.columns:
                _col = col.replace("_", " ")
                values = (
                    kwargs.get(col)
                    if isinstance(kwargs.get(col), list)
                    else [kwargs.get(col)]
                )
                for value in values:
                    if value not in self._obj[_col].values:
                        raise ValueError(f"{value} is not in {_col}")
                filters[_col] = values
            else:
                raise ValueError(f"{col} is not in frame")

        self.filters = filters

        # filter the frame
        if inverse:
            frame = self._obj[
                self._obj.isin(filters).sum(axis=1) != len(filters.keys())
            ]
        else:
            frame = self._obj[
                self._obj.isin(filters).sum(axis=1) == len(filters.keys())
            ]

        return frame

    def nthsmallest(self, n=0, axis=0, **kwargs):
        """
        Return a Pandas Series from a Pandas DataFrame with the nth smallest values
        over the requested axis.

        Parameters
        ----------
        self : Series or DataFrame
        n: zero based n, default 0
        axis: axis for the function to be applied on, default 0

        Returns
        -------
        Series

        Example
        -------

        df
            | column_1  | column_2  | column_3  |
        -----------------------------------------
        0   | 1         | 4         | 6         |
        1   | 2         | 2         | 2         |
        2   | 1         | 3         | 3         |
        3   | 1         | 4         | 5         |
        4   | 2         | 1         | 3         |
        5   | 3         | 2         | 4         |

        >> df.blue.nthsmallest(n=2, axis=0)

        column_1   1
        column_2   2
        column_3   4
        
        >> df.blue.nthsmallest(n=1, axis=1)

        0   4
        1   2
        2   3
        3   4
        4   2
        5   3
        """
        array = self._obj.to_numpy()
        array = np.partition(array, n, axis=axis)
        if axis == 0:
            index = self._obj.columns
            array = array[n : n + 1, :].flatten()
        else:
            index = self._obj.index
            array = array[:, n : n + 1].flatten()
        return pd.Series(index=index, data=array)

    def nthlargest(self, n=0, axis=0, **kwargs):
        """
        Return a Pandas Series from a Pandas DataFrame with the nth largest values
        over the requested axis.

        Parameters
        ----------
        self : Series or DataFrame
        n: zero based n, default 0
        axis: axis for the function to be applied on, default 0

        Returns
        -------
        Series

        Example
        -------

        df
            | column_1  | column_2  | column_3  |
        -----------------------------------------
        0   | 1         | 4         | 6         |
        1   | 2         | 2         | 2         |
        2   | 1         | 3         | 3         |
        3   | 1         | 4         | 5         |
        4   | 2         | 1         | 3         |
        5   | 3         | 2         | 4         |

        >> df.blue.nthlargest(n=2, axis=0)

        column_1   2
        column_2   3
        column_3   4
        
        >> df.blue.nthlargest(n=1, axis=1)

        0   4
        1   2
        2   3
        3   4
        4   2
        5   3
        """
        array = self._obj.to_numpy()

        # not the smallest but the opposite
        n = array.shape[axis] - (n + 1)

        array = np.partition(array, n, axis=axis)
        if axis == 0:
            index = self._obj.columns
            array = array[n : n + 1, :].flatten()
        else:
            index = self._obj.index
            array = array[:, n : n + 1].flatten()
        return pd.Series(index=index, data=array)

    class stats:
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def index(self):
            return bluebelt.statistics.hypothesis_testing.index()

        # hypothesis testing
        def dagostino_pearson(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.DAgostinoPearson(
                self._obj, alpha=alpha
            )

        normal_distribution = dagostino_pearson

        def anderson_darling(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.AndersonDarling(
                self._obj, alpha=alpha
            )

        def std_within(self, how=None, observations=2, **kwargs):
            return bluebelt.statistics.std.StdWithin(
                self._obj, how=how, observations=observations, **kwargs
            )

        def one_sample_t(self, popmean=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.OneSampleT(
                self._obj, popmean=popmean, alpha=alpha, **kwargs
            )

        def wilcoxon(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Wilcoxon(
                self._obj, alpha=alpha, **kwargs
            )

        def equal_means(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.EqualMeans(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        def two_sample_t(
            self, columns=None, related=False, confidence=0.95, alpha=0.05, **kwargs
        ):
            return bluebelt.statistics.hypothesis_testing.TwoSampleT(
                self._obj,
                columns=columns,
                related=related,
                confidence=confidence,
                alpha=alpha,
                **kwargs,
            )

        def mann_whitney(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.MannWhitney(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        def anova(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Anova(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        def kruskal(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.KruskalWallis(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        kruskal_wallis = kruskal

        def levene(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Levene(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        def bartlett(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Bartlett(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        def f_test(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.FTest(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        def equal_variances(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.EqualVariances(
                self._obj, columns=columns, alpha=alpha, **kwargs
            )

        equal_var = equal_variances

        def correlation(self, columns=None, confidence=0.95, **kwargs):
            return bluebelt.statistics.basic.Correlation(
                self._obj, columns=columns, confidence=confidence
            )
