# File:    <repo>/src/reflect/runtime_os.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `runtime_os` module provides runtime operating system related reflection
utilities.
"""

import os


def is_windows_compatible():
    """
    Determines if the runtime operating system is Windows NT compatible.
    """
    return bool(os.name == "nt")


def is_posix_compatible():
    """
    Determines if the runtime operating system is POSIX compatible.
    """
    return bool(os.name == "posix")


__all__ = [
    is_windows_compatible,
    is_posix_compatible,
]
