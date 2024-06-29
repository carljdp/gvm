# File:    <repo>/src/reflect/script.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `script` module provides runtime script environment reflection utilities.
"""


import os
import pwd


def is_invoked() -> bool:
    """Returns True if this script is run directly, False if imported as a module."""
    return __name__ == "__main__"


def is_imported() -> bool:
    """Returns True if this script is imported as a module, False if run directly."""
    return not is_invoked()


def is_privileged() -> bool:
    """
    Check if the script was invoked with temporary elevated privileges.

    The method to determine if a script was invoked in a temporary elevated
    state is platform dependent:

    - On POSIX systems, a command can run with elevated privileges if invoked by
    a user with `sudo` privileges. The command then runs with the privileges of
    the specified user (default is root) as indicated by the `sudo` command.

    - On Windows systems, a process can run with elevated privileges if an
    administrative token is granted to the process. The process then runs with
    the privileges of an administrator, as confirmed by the UAC (User Account
    Control) prompt.

    Returns:
        - `True` if the script is invoked by a privileged process,
        - `False` otherwise.
    """
    raise NotImplementedError("Not yet implemented.")


def get_owner(script_path):
    """Return the username of the owner of the script file."""
    return pwd.getpwuid(os.stat(script_path).st_uid).pw_name


__all__ = [
    is_invoked,
    is_imported,
    is_privileged,
    get_owner,
]
