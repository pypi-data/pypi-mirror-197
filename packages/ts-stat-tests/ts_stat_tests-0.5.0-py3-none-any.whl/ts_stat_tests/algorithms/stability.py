# ---------------------------------------------------------------------------- #
#                                                                              #
#    Setup                                                                  ####
#                                                                              #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Imports                                                                   ####
# ---------------------------------------------------------------------------- #


# Python ----
from typing import Union

# Packages ----
import numpy as np
import pandas as pd
from statsmodels.tools.validation import (
    array_like,
    bool_like,
    float_like,
    int_like,
    string_like,
)
from tsfeatures import lumpiness as ts_lumpiness, stability as ts_stability
from typeguard import typechecked

# ---------------------------------------------------------------------------- #
# Exports                                                                   ####
# ---------------------------------------------------------------------------- #


__all__ = ["stability", "lumpiness"]


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Algorithms                                                             ####
#                                                                              #
# ---------------------------------------------------------------------------- #


# -----------------------------------------------------------------------------#
# Stability                                                                 ####
# -----------------------------------------------------------------------------#


@typechecked
def stability(data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1) -> float:
    """
    !!! Summary

        The stability test is a diagnostic tool used in time series forecasting to evaluate whether a forecasting model's performance remains consistent over time. The test assesses whether the parameters of the model remain stable over time or if they change significantly, which can indicate that the model's predictive ability may deteriorate.

    ???+ Info "Details"

        Computes feature of a time series based on tiled (non-overlapping) windows. Means or variances are produced for all tiled windows. Then stability is the variance of the means, while lumpiness is the variance of the variances.

        The equation for $stability$ is:

        $$
        stability = \\frac{1}{n-1} \\sum_{i=1}^{n}(\\overline{x_i} - \\overline{x})^2
        $$

        where:

        - $n$ is the number of segments
        - $\\overline{x_i}$ is the mean of segment $i$
        - $\\overline{x}$ is the mean of the entire time series.

        The stability test involves dividing the time series data into two or more subsets and fitting the forecasting model separately to each subset. The subsets should be chosen in such a way that they represent different periods of the time series, such as the first half and the second half, or every other year. The model is then used to forecast the remaining portion of the time series for each subset, and the accuracy of the forecasts is compared across the subsets.

        If the model's performance remains consistent across the subsets, then the model is considered to be stable. However, if there is a significant difference in the accuracy of the forecasts across the subsets, then this indicates that the model's parameters may be changing over time, and the model may not be suitable for forecasting future data.

        The stability test can be implemented in Python using time series forecasting libraries such as `statsmodels` or `prophet`. The time series data is split into subsets using a suitable method, such as a rolling window or a fixed interval. The model is then fitted to each subset and the accuracy of the forecasts is compared using appropriate metrics such as mean absolute error (MAE) or mean squared error (MSE). If the difference in the forecast accuracy is statistically significant, then the model may need to be updated or revised to improve its stability.

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            Frequency of the time series

    Returns:
        (float):
            Variance of the means of tiled windows.

    !!! Success "Credit"
        All credit goes to the [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py) library.

    ???+ Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(stability(data))
        12702.672087912088
        ```

    ??? question "References"
        1. ...

    ??? tip "See Also"
        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)
    """
    return ts_stability(x=data, freq=freq)["stability"]


# ------------------------------------------------------------------------------#
# Lumpiness                                                                  ####
# ------------------------------------------------------------------------------#


@typechecked
def lumpiness(data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1) -> float:
    """
    !!! Summary

        The lumpiness test is a measure of the variability of the time series' mean value over different time intervals. It aims to identify if the time series has a tendency to exhibit large or small fluctuations in the mean value across time intervals. A time series is said to have high lumpiness if the variance of the series mean values is large, and low lumpiness if the variance of the mean values is small.

    ???+ Info "Details"

        The lumpiness test calculates the variance of the time series' mean value over non-overlapping time intervals. If the variance of the mean values is greater than a certain threshold, then the time series is considered to have high lumpiness. Conversely, if the variance of the mean values is lower than the threshold, then the time series is considered to have low lumpiness.

        The mathematical equation for the lumpiness function in Python is:

        - Let $x$ be a time series of length $n$ with a given $freq$. We can divide $x$ into $k$ non-overlapping segments of length $freq$. Then, we calculate the variance of each segment $i$ as:

            $$
            var_i = \\frac{1}{freq-1} \\times \\sum_{j=1}^{freq} \\left( x_{(i-1) \\times freq + j} - \\overline{x_i} \\right) ^2
            $$

            where:

            - $\\overline{x_i}$ is the mean of segment $i$.

        - Next, we calculate the variance of the variances of each segment as:

            $$
            lumpiness = \\frac{1}{k-1} \\times \\sum_{i=1}^{k} \\left( var_i - \\overline{var} \\right) ^2
            $$

            where:

            - $\\overline{var}$ is the mean of the variances of each segment.

        - The lumpiness value is a measure of how much the variance of the time series changes across different segments of the same length freq. If the time series has a stable variance over different segments, then the lumpiness value will be low.

        The lumpiness test is useful for identifying patterns in the time series that may be indicative of underlying phenomena. For example, if a time series exhibits high lumpiness, it may suggest that the mean value of the time series is subject to changes in trends or seasonal fluctuations, which can be useful in forecasting future values of the time series.

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            Frequency of the time series

    Returns:
        (float):
            Variance of the means of tiled windows.

    !!! Success "Credit"
        All credit goes to the [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py) library.

    ???+ Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(lumpiness(data))
        5558930.856730431
        ```

    ??? question "References"
        1. ...

    ??? tip "See Also"
        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)
    """
    return ts_lumpiness(x=data, freq=freq)["lumpiness"]
