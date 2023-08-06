from typing import Any, Dict, List, Optional, Union

from typeguard import typechecked


@typechecked
def generate_error_message(
    parameter_name: str,
    value_parsed: Any,
    options: Union[
        Dict[str, str],
        Dict[str, List[str]],
        Dict[str, List[Union[str, int, float]]],
    ],
) -> str:
    error_message = (
        f"Invalid option for `{parameter_name}` parameter: '{value_parsed}'.\n"
    )
    for key, value in options.items():
        error_message += f"For the '{key}' option, use one of: '{value}'.\n"
    return error_message


@typechecked
def is_almost_equal(
    first: float,
    second: float,
    places: Optional[int] = None,
    msg: Optional[str] = None,
    delta: Optional[float] = None,
) -> bool:
    """
    Inspiration from Python's UnitTest function `assertAlmostEqual`.
    See: https://github.com/python/cpython/blob/3.11/Lib/unittest/case.py
    """
    if first == second:
        return True
    if places is not None and delta is not None:
        print("entered")
        raise ValueError(f"Specify `delta` or `places`, not both.")
    diff = abs(first - second)
    if delta is not None:
        if diff <= delta:
            return True
        standard_msg = f"{first} != {second} within {delta} delta ({diff} difference)"
    else:
        if places is None:
            places = 7
        if round(diff, places) == 0:
            return True
        standard_msg = f"{first} != {second} within {places} places ({diff} difference)"
    msg = msg or standard_msg
    return False


@typechecked
def assert_almost_equal(
    first: float,
    second: float,
    places: Optional[int] = None,
    msg: Optional[str] = None,
    delta: Optional[float] = None,
) -> None:
    """
    Inspiration from Python's UnitTest function `assertAlmostEqual`.
    See: https://github.com/python/cpython/blob/3.11/Lib/unittest/case.py
    """
    if first == second:
        return None
    if places is not None and delta is not None:
        print("entered")
        raise ValueError(f"Specify `delta` or `places`, not both.")
    diff = abs(first - second)
    if delta is not None:
        if diff <= delta:
            return None
        standard_msg = f"{first} != {second} within {delta} delta ({diff} difference)"
    else:
        if places is None:
            places = 7
        if round(diff, places) == 0:
            return None
        standard_msg = f"{first} != {second} within {places} places ({diff} difference)"
    msg = msg or standard_msg
    raise AssertionError(msg)
