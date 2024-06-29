# File:    <repo>/src/gvm/main.py
# Date:    2024-06-29
# License: MIT License
# Author:  Carl J du Preez <carljdp@gmail.com>

"""
This `main` sub module of the `gvm` package contains the implementation of the
Gradle Version Manager (GVM) CLI.

This (mainly CLI-aimed) utility script is intended to help developers manage
multiple Gradle versions on a single machine. It can:
- List available Gradle versions
- Switch between them by creating a symbolic link to the desired version.

"""

import os
import sys
import argparse
import re
from typing import Optional, Union


from reflect import script, location, platform, runtime_env, runtime_os


# Fallback to C: if system drive letter cannot be determined
SYSTEM_DRIVE_LETTER = location.get_system_drive_letter() or 'C'

if platform.is_windows_system() and not runtime_os.is_posix_compatible():
    SYSTEM_DRIVE_LETTER = SYSTEM_DRIVE_LETTER.upper()
    GRADLE_WRAPPER_DISTS_DIR = f"{SYSTEM_DRIVE_LETTER}:\\Tools\\Gradle\\wrapper\\dists"
    CURRENT_GRADLE_SYMLINK = f"{SYSTEM_DRIVE_LETTER}:\\Tools\\Gradle\\current"
elif (platform.is_windows_system() and runtime_os.is_posix_compatible()) or runtime_env.is_wsl():
    SYSTEM_DRIVE_LETTER = SYSTEM_DRIVE_LETTER.lower()
    GRADLE_WRAPPER_DISTS_DIR = f"/mnt/{SYSTEM_DRIVE_LETTER}/Tools/Gradle/wrapper/dists"
    CURRENT_GRADLE_SYMLINK = f"/mnt/{SYSTEM_DRIVE_LETTER}/Tools/Gradle/current"
else:
    print("Unsupported platform, OS or runtime environment.")
    sys.exit(1)


def contains_sub_bin_dir(path: str) -> bool:
    return bool(any(d == "bin" for d in os.listdir(path)))


def contains_gradle_bin_file(path: str) -> bool:
    return bool(any(f.startswith("gradle") for f in os.listdir(path)))


def ends_like_unzip_hash_dir(path: str) -> bool:
    return bool(re.search(r"[a-z0-9]{25}$", path))


def ends_like_gradle_dir(path: str) -> bool:
    return bool(re.search(r"gradle-\d(?:\.\d)+-(?:all|bin)$", path))


def is_gradle_version_dir(dirName: str) -> bool:
    return bool(re.match(r"^gradle-\d(?:\.\d)+-(?:all|bin)$", dirName))


def contains_only_one_dir(path: str) -> bool:
    return len([d for d in os.listdir(path)
               if os.path.isdir(os.path.join(path, d))]) == 1


def find_gradle_version_paths_from(
        start_dir: str, versions: Optional[list[str]] = None) -> list[str]:
    if versions is None:
        versions = []

    try:
        maybeGradleVerDirs = [
            d for d in os.listdir(start_dir) if os.path.isdir(
                os.path.join(
                    start_dir, d))]
    except PermissionError:
        print(
            f"Permission denied: Unable to list directories in '{start_dir}'.",
            file=sys.stderr)
        return versions

    for maybeGradleVerDir in maybeGradleVerDirs:
        maybeGradleVerDirPath = os.path.join(start_dir, maybeGradleVerDir)

        if contains_only_one_dir(maybeGradleVerDirPath):
            maybeHashDir = os.path.join(
                maybeGradleVerDirPath,
                os.listdir(maybeGradleVerDirPath)[0])
            if ends_like_unzip_hash_dir(maybeHashDir):
                versions.extend(find_gradle_version_paths_from(maybeHashDir))
        else:
            if contains_sub_bin_dir(maybeGradleVerDirPath) and contains_gradle_bin_file(
                    os.path.join(maybeGradleVerDirPath, "bin")):
                versions.append(maybeGradleVerDirPath)

    return versions


def get_version_from_path(path: str) -> Optional[str]:
    path_parts = path.split(os.sep)
    path_parts.reverse()
    for path_part in path_parts:
        if is_gradle_version_dir(path_part):
            return path_part.split("-")[1]
    return None


def switch_gradle_version(
        version: str,
        dry_run: bool = False,
        verbose: bool = False) -> None:
    gradle_version_paths = find_gradle_version_paths_from(
        GRADLE_WRAPPER_DISTS_DIR, [])
    versions = [get_version_from_path(
        path) for path in gradle_version_paths if get_version_from_path(path)]

    matching_versions = [
        v for v in gradle_version_paths if version == get_version_from_path(v)]

    if not matching_versions:
        raise FileNotFoundError(f"Gradle version '{version}' does not exist.")

    pseudo_gradle_home_dir = matching_versions[0]
    pseudo_gradle_bin_dir = os.path.join(pseudo_gradle_home_dir, "bin")

    if dry_run:
        print(f"[DRY-RUN] Would switch to Gradle version: {version}")
        print(
            f"[DRY-RUN] Would create symlink from {pseudo_gradle_bin_dir} to {CURRENT_GRADLE_SYMLINK}")
        return

    if os.path.exists(CURRENT_GRADLE_SYMLINK) or os.path.islink(
            CURRENT_GRADLE_SYMLINK):
        try:
            os.remove(CURRENT_GRADLE_SYMLINK)
            if verbose:
                print(f"Removed existing symlink: {CURRENT_GRADLE_SYMLINK}")
        except PermissionError as e:
            print(f"Permission denied: {e}")
            sys.exit(1)

    try:
        os.symlink(pseudo_gradle_bin_dir, CURRENT_GRADLE_SYMLINK)
        if verbose:
            print(
                f"Created symlink from {pseudo_gradle_bin_dir} to {CURRENT_GRADLE_SYMLINK}")
    except OSError as e:
        print(f"Error creating symlink: {e}")
        sys.exit(1)

    print(f"Switched to Gradle version: {version}")


def list_gradle_versions(start_dir: str) -> list[str]:
    versions = find_gradle_version_paths_from(start_dir, [])
    return [get_version_from_path(v)
            for v in versions if get_version_from_path(v)]


def main():
    parser = argparse.ArgumentParser(
        description="Switch between Gradle versions.")
    parser.add_argument(
        "--use",
        metavar="VERSION",
        help="The Gradle version to switch to.")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available Gradle versions.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the intended actions without making any changes.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print extra information about the actions being performed.")
    parser.add_argument(
        "--log-level",
        type=int,
        choices=[
            0,
            1,
            2],
        help="Set the log level: 0 for errors, 1 for info, 2 for debug.")

    args = parser.parse_args()

    verbose = args.verbose or (args.log_level and args.log_level > 0)

    if args.list:
        versions = list_gradle_versions(GRADLE_WRAPPER_DISTS_DIR)
        unique_versions = sorted(
            set(versions), key=lambda v: [
                int(part) for part in v.split('.')])

        print("Available Gradle versions:")
        for version in unique_versions:
            print(f" - {version}")

    elif args.use:
        if not script.is_running_as_privileged_user():
            print(
                "To write the Gradle version symlink, this script must be run as a privileged user.")
            sys.exit(1)

        try:
            switch_gradle_version(
                args.use,
                dry_run=args.dry_run,
                verbose=verbose)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
else:
    pass
