# File:    <repo>/src/reflect/platform.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `platform` module provides runtime platform related reflection utilities.
"""

import platform


def is_darwin_system():
    """
    Returns True if the current platform is Darwin based.
    """
    return bool(platform.system() == "Darwin")


def is_linux_system():
    """
    Returns True if the current platform is Linux Kernel based.
    """
    return bool(platform.system() == "Linux")


def is_windows_system():
    """
    Returns True if the current platform is Windows NT based.
    """
    return bool(platform.system() == "Windows")


__all__ = [
    is_darwin_system,
    is_linux_system,
    is_windows_system,
]
