# File:    <repo>/src/reflect/machine.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>


"""
This `machine` module provides machine related reflection utilities.
"""

from reflect import runtime_env


def is_not_physical_machine():
    """
    Check if the current runtime environment is running in a virtualized,
    containerized, sandboxed, emulated, or otherwise non-physical machine.
    Returns:
        bool: True if the current environment is not a physical machine,
        False otherwise.
    """
    return any([
        runtime_env.is_wsl(),
        runtime_env.is_docker_container(),
        runtime_env.is_windows_sandbox(),
        runtime_env.is_hypervisor(),
    ])


def is_physical_machine():
    """
    Check if the current runtime environment is running on a real, tangible,
    physical machine.

    Returns:
        bool: True if the current environment is a physical machine,
        False otherwise.
    """
    return not is_not_physical_machine()


__all__ = [
    is_physical_machine,
    is_not_physical_machine,
]
