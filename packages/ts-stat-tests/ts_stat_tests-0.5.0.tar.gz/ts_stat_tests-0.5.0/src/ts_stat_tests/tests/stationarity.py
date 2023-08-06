# from pmdarima.arima.stationarity import PPTest, ADFTest, KPSSTest
# from statsmodels.tsa.api import adfuller, kpss
# """
# For a really good article on ADF & KPSS tests, check: [When A Time Series Only Quacks Like A Duck: Testing for Stationarity Before Running Forecast Models. With Python. And A Duckling Picture.](https://towardsdatascience.com/when-a-time-series-only-quacks-like-a-duck-10de9e165e)
# """


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Setup                                                                  ####
#                                                                              #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Imports                                                                   ####
# ---------------------------------------------------------------------------- #


# Python ----
from typing import Dict, Tuple, Union

# Packages ----
from statsmodels.tools.validation import (
    array_like,
    bool_like,
    dict_like,
    float_like,
    int_like,
    string_like,
)

# Locals ----
from ts_stat_tests.algorithms.stationarity import (
    adf as _adf,
    kpss as _kpss,
    pp as _pp,
    rur as _rur,
    za as _za,
)

# ---------------------------------------------------------------------------- #
# Exports                                                                   ####
# ---------------------------------------------------------------------------- #

__all__ = ["stationarity", "is_stationary"]


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Tests                                                                  ####
#                                                                              #
# ---------------------------------------------------------------------------- #


def stationarity(x: array_like):
    pass


def is_startionary(x: array_like):
    pass
