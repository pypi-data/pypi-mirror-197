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
from typeguard import typechecked

# Locals ----
from ts_stat_tests.algorithms.stability import (
    lumpiness as _lumpiness,
    stability as _stability,
)

# ---------------------------------------------------------------------------- #
# Exports                                                                   ####
# ---------------------------------------------------------------------------- #


__all__ = ["is_stable", "is_lumpy"]


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Algorithms                                                             ####
#                                                                              #
# ---------------------------------------------------------------------------- #


# -----------------------------------------------------------------------------#
# Stability                                                                 ####
# -----------------------------------------------------------------------------#


@typechecked
def is_stable(
    data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1, alpha: float = 0.5
) -> bool:
    """
    !!! Summary
        Check whether a data series is stable or not.

    ???+ Info "Details"
        For full documentation, see:

        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            The frequency of the time series. Defaults to `1`.
        alpha (float, optional):
            The value, above which, the data will be stable. Defaults to `0.5`.

    Returns:
        (bool):
            A confirmaiont of whether or not the data is stable.

    !!! Success "Credit"
        All credit goes to the [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py) library.

    ???+ Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(is_stable(data))
        True
        ```
    """
    return True if _stability(data=data, freq=freq) > alpha else False


# ------------------------------------------------------------------------------#
# Lumpiness                                                                  ####
# ------------------------------------------------------------------------------#


@typechecked
def is_lumpy(
    data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1, alpha: float = 0.5
) -> bool:
    """
    !!! Summary
        Check whether a data series is lumpy or not.

    ???+ Info "Details"
        For full documentation, see:

        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            The frequency of the time series. Defaults to `1`.
        alpha (float, optional):
            The value, above which, the data will be stable. Defaults to `0.5`.

    Returns:
        (bool):
            A confirmaiont of whether or not the data is lumpy.

    !!! Success "Credit"
        All credit goes to the [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py) library.

    ???+ Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(is_lumpy(data))
        True
        ```
    """
    return True if _lumpiness(data=data, freq=freq) > alpha else False
