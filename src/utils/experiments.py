# File:    <repo>/src/utils/module.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `experiments` sub module of the `utils` package provides, uhm, experiments.
"""

# -----------------------------------------------------------

from functools import wraps
import sys
__all__ = []
this = sys.modules[__name__]

# I was going somewhere with ^^^ this, but I forgot where.


# -----------------------------------------------------------


# I JUST SAW THIS SOMEWHERE - HAVENT GOT IT WORKING YET
#


def type_check(arg_types, return_type):
    """
    Decorator that checks the types of the arguments and the return value of a
    function.

    Args:
        arg_types (tuple): The types of the arguments.
        return_type (type): The type of the return value.

    Returns:
        function: The decorated function.

    Raises:
        TypeError: If the types of the arguments or the return value do not match
            the specified types.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for (arg, arg_type) in zip(args, arg_types):
                if not isinstance(arg, arg_type):
                    raise TypeError(
                        f"Argument {arg} does not match {arg_type}")
            result = func(*args, **kwargs)
            if not isinstance(result, return_type):
                raise TypeError(
                    f"Return value {result} does not match {return_type}")
            return result
        return wrapper
    return decorator


# -----------------------------------------------------------
