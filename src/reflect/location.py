# File:    <repo>/src/reflection/location.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `location` module provides location reflection utilities.
"""

import sys
import os
import platform
import subprocess


def get_system_drive_letter():
    """
    Get the system drive letter.

    On WSL2, returns the Windows system drive letter if possible.

    On Windows, returns the system drive letter.

    """
    if platform.system() == "Linux":
        # Check if running under WSL
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    # Running under WSL
                    drive = subprocess.check_output(
                        "cmd.exe /c echo %SystemDrive%", shell=True).decode().strip()
                    return drive.strip(':')
        except Exception as e:
            print(e, file=sys.stderr)
            return None
    elif platform.system() == "Windows":
        return os.getenv('SystemDrive').strip(':')
    return None


def get_root_and_path(schema="file://"):
    """
    Get the root drive letter and the path of the script.

    On WSL2, returns [schema, "wsl.localhost/Debian/", "/path/to/script.py"]

    On Windows, returns [schema, "C:/", "/path/to/script.py"]

    """

    script_path = os.path.abspath(__file__).strip('/')
    if platform.system() == "Linux":
        # Check if running under WSL
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    # Convert the Linux path to a Windows path
                    wsl_path = subprocess.check_output(
                        # `-m` flag:
                        # translate from a WSL path to a Windows path, with '/'
                        ['wslpath', '-m', f"/{script_path}"]).decode().strip()

                    network_root = wsl_path.replace(script_path, "")[2:]

                    return [schema, network_root, script_path]

        except Exception as e:
            return [schema, None, script_path]
    elif platform.system() == "Windows":
        drive_letter = os.path.splitdrive(script_path)
        return [schema, drive_letter, script_path.replace("\\", "/")]
    return [schema, None, script_path]
