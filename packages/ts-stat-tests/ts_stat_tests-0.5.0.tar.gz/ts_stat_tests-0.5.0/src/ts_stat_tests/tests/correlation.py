# ---------------------------------------------------------------------------- #
#                                                                              #
#    Setup                                                                  ####
#                                                                              #
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Imports                                                                   ####
# ---------------------------------------------------------------------------- #


# Python ----


from typing import Tuple, Union

# Packages ----
import numpy as np
from statsmodels.tools.validation import array_like

# Locals ----
from src.ts_stat_tests.algorithms.correlation import (
    abg as _abg,
    acf as _acf,
    alb as _alb,
    alm as _alm,
    ccf as _ccf,
    pacf as _pacf,
)
from src.ts_stat_tests.utils.errors import (
    generate_error_message as _generate_error_message,
)

# from ts_stat_tests.utils.dict_helpers import dict_reverse_key_values


# ---------------------------------------------------------------------------- #
# Exports                                                                   ####
# ---------------------------------------------------------------------------- #


__all__ = ["correlation", "is_correlated"]


# ---------------------------------------------------------------------------- #
#                                                                              #
#    Tests                                                                  ####
#                                                                              #
# ---------------------------------------------------------------------------- #


def correlation(
    x: array_like, algorithm: str, **kwargs
) -> Union[np.ndarray, Tuple[np.ndarray, ...]]:
    options = {
        "acf": ["acf", "auto", "ac"],
        "pacf": ["pacf", "partial", "pc"],
        "alb": ["alb", "acorr_ljungbox", "acor_lb", "a_lb", "lb", "ljungbox"],
        "alm": ["alm", "acorr_lm", "a_lm", "lm"],
        "ccf": ["ccf", "cross", "cross_correlation", "cross-correlation", "cc"],
    }
    # options_r = dict_reverse_key_values(options)
    # if algorithm in options_r.keys():
    #     return locals().get(options_r.get(algorithm))(x=x, **kwargs)
    if algorithm in options["acf"]:
        return _acf(x=x, **kwargs)  # type: ignore
    elif algorithm in options["pacf"]:
        return _pacf(x=x, **kwargs)  # type: ignore
    elif algorithm in options["alb"]:
        return _alb(x=x, **kwargs)  # type: ignore
    elif algorithm in options["alm"]:
        return _alm(resid=x, **kwargs)  # type: ignore
    elif algorithm in options["ccf"]:
        return _ccf(x=x, **kwargs)  # type: ignore
    else:
        raise ValueError(
            _generate_error_message(
                parameter_name="algorithm",
                value_parsed=algorithm,
                options=options,
            )
        )


def is_correlated():
    pass
