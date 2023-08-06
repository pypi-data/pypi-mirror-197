"""
This module contains utility functions for the rest of the library.
It is private and should not be imported by the user.
"""
from typing import Callable, Dict, Tuple, Union


def _get_type_error(
    name: str, allowed_types: Union[type, Tuple[type]], bad_data) -> TypeError:
    # Generates a TypeError based on the name of the data,
    # the allowed data types, and the type of the erroneous data.
    if allowed_types is None or isinstance(allowed_types, type):
        # Turns a standalone type into a 1-tuple.
        allowed_types = (allowed_types,)
    allowed_types_str_parts = []
    allowed_types_count = len(allowed_types)
    for i, _type in enumerate(allowed_types):
        # None does not have __name__ for some reason.
        type_name = _type.__name__ if _type is not None else "None"
        allowed_types_str_parts.append(f"'{type_name}'")
        if i == allowed_types_count - 2:
            # Penultimate allowed data type. Natural English.
            allowed_types_str_parts.append(" or ")
        if i < allowed_types_count - 2:
            allowed_types_str_parts.append(", ")
    bad_type_name = type(bad_data).__name__ if bad_data is not None else "None"
    allowed_types_str = "".join(allowed_types_str_parts)
    return TypeError(
        f"'{name}' must be of type {allowed_types_str}, not '{bad_type_name}'")


def _method_type_check(
    identifier: str, allowed_types: Union[type, Tuple[type]]) -> Callable:
    # Class method decorator to ensure entered value is a certain type.
    def decorator(method: Callable) -> Callable:
        def wrapper(obj: object, value) -> None:
            nonlocal allowed_types # May be needed to reassign.
            if allowed_types is None or isinstance(allowed_types, type):
                # Turns a standalone type into a 1-tuple.
                allowed_types = (allowed_types,)
            for _type in allowed_types:
                if _type is None:
                    if value is None:
                        break
                elif isinstance(value, _type):
                    break
            else:
                # The value does not match any allowed types.
                raise _get_type_error(identifier, allowed_types, value)
            method(obj, value)
        return wrapper
    return decorator


def _convert_units(
    value: Union[int, float], _from: str, to: str,
    units: Dict[str, Union[int, float]]) -> Union[int, float]:
    # Performs unit conversion based on a dict of units and relative values.
    return value * (units[_from] / units[to])


def _keep_in_range(
    value: Union[int, float], _min: Union[int, float] = float("-inf"),
    _max: Union[int, float] = float("inf")) -> int:
    # Ensures value is not less than min or greater than max.
    # Sets to min if less than min, to max if more than max.
    return max(min(value, _max), _min)
