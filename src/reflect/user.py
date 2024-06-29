# File:    <repo>/src/reflect/user.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `user` module provides user related reflection utilities.
"""

import os
import pwd
import sys


def get_uid(username=None):
    """
    Get the User ID of the specified user name. Defaults to the current user.

    The returned user is not necessarily the same as the user the script is
    running as.

    Args:
        username (str, optional): The username to get the user ID of.
            Defaults to the current user.

    Returns:
        int: The user ID of the user.
        None: If the user ID could not be resolved.
    """
    found_uid = None
    try:
        user_to_check = username if username else os.getlogin()
        found_uid = pwd.getpwnam(user_to_check).pw_uid
    except BaseException as e:
        print(
            "Could not resolve username {} back to a valid uid".format(username),
            file=sys.stderr)
        print(e, file=sys.stderr)
    return found_uid


def get_username(uid=None):
    """
    Get the specified user's username. Defaults to the current user.

    The returned user is not necessarily the same as the user the script is
    running as.

    Args:
        uid (int, optional): The User ID to get the username of.
            Defaults to the current user.

    Returns:
        str: The username of the user.
        None: If the username could not be resolved.
    """
    found_username = None
    try:
        user_id_to_check = uid if uid else os.geteuid()
        found_username = pwd.getpwuid(user_id_to_check).pw_name
    except BaseException as e:
        print(
            "Could not resolve uid {} back to a valid username".format(id),
            file=sys.stderr)
        print(e, file=sys.stderr)
    return found_username


def get_home_dir(uid=None):
    """
    Get the home directory of the specified user.

    This function is does not check if the returned home directory exists.

    Args:
        uid (int, optional): The user ID to get the home directory of.
            Defaults to the current user.

    Returns:
        str: The home directory of the user.
        None: If the home directory could not be resolved, or the user does not
            have a home directory.
    """
    found_home_dir = None
    try:
        user_id_to_check = uid if uid else os.geteuid()
        found_home_dir = pwd.getpwuid(user_id_to_check).pw_dir
    except BaseException as e:
        print(
            "Could not resolve uid {} back to a valid home directory".format(id),
            file=sys.stderr)
        print(e, file=sys.stderr)
    return found_home_dir


def is_privileged(uid=None):
    """
    Checks if the specified user is privileged.

    Args:
        uid (int, optional): The user ID to check.
            Defaults to the current user.

    Returns:
        bool: True if the user is privileged, False otherwise.

    """
    result = False
    try:
        user_id_to_check = uid if uid else os.geteuid()
        result = user_id_to_check == 0
    except BaseException as e:
        print("Could not check if user is privileged", file=sys.stderr)
        print(e, file=sys.stderr)
    return result



__all__ = [
    get_uid,
    get_username,
    get_home_dir,
    is_privileged,
]
