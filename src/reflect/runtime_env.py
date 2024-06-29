# File:    <repo>/src/reflection/runtime_env.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `runtime_env` module provides runtime environment related reflection
utilities.
"""

import sys
import os
import platform
import psutil


def is_wsl():
    """
    Check if the current environment is Windows Subsystem for Linux (WSL).

    Returns:
        bool: True if the current environment is WSL,
            False otherwise.
    """
    try:
        with open('/proc/version', 'r') as f:
            return 'microsoft' in f.read().lower()
    except BaseException as e:
        print(e, file=sys.stderr)
    return False


def is_docker_container():
    """
    Check if the current environment is Docker.

    Returns:
        bool: True if the current environment is Docker,
            False otherwise.
    """
    path = '/proc/1/cgroup'
    if os.path.exists(path):
        with open(path, 'r') as f:
            if 'docker' in f.read():
                return True
    return os.path.exists('/.dockerenv')


def is_windows_sandbox():
    """
    Check if the current environment is Windows Sandbox.

    Returns:
        bool: True if the current environment is Windows Sandbox,
            False otherwise.
    """
    # not using our own implementation because it might cause circular imports
    if platform.system() == 'Windows':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"SYSTEM\CurrentControlSet\Control\Sandbox"
                                ) as key:
                return True
        except (ImportError, FileNotFoundError, OSError):
            return False
    return False


def is_hypervisor_like(
        virtual_machines=[
            'virtualbox',
            'vmware',
            'qemu',
            'kvm',
            'hyper-v'
        ]):
    """
    Check if the current environment is a virtual machine or hypervisor of a
    specific setof types passed as a list.

    Args:
        virtual_machines (list, optional): A list of strings representing the
            device names of virtual machines or hypervisors. Defaults to a list
            of common virtual machine and hypervisor names.

    Returns:
        bool: True if the current environment is a virtual machine,
            False otherwise.
    """
    for device in psutil.disk_partitions(all=True):
        if any(vm in device.device.lower() for vm in virtual_machines):
            return True
    return False


__all__ = [
    is_wsl,
    is_docker_container,
    is_windows_sandbox,
    is_hypervisor_like,
]
