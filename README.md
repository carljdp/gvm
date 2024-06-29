# gvm

An uninformed attempt to create a Gradle Version Manager (GVM) for Windows.

---

## Dev Guide

Requirements:
- Python 3.8 or higher
- pip (to install poetry)
- poetry

### WSL2

> There's no particular reason to use WSL2, but it's the environment I'm using to develop this project.


1. Clone the repository to your WSL2 projects directory

```bash

git clone https://github.com/carljdp/gvm.git

cd ./gvm

```

2. Create and activate a virtual environment

```bash

python3 -m venv .venv

source .venv/bin/activate

```

3. Install dependencies

```bash

poetry install

```

4. Build standalone executable

- requires `pip install pyinstaller`

You can build a standalone executable for both Windows and Linux, but you need to build them individually from their respective platforms.


```bash

pyinstaller --onefile src/gvm/main.py

```


---

## Usage


To run a WSL2 python script from windows powershell, you can do the following:

> TODO: This used to work before I started refactoring into separate modules, 
> and now it seems windows can't find the modules. 🤔

```ps1

cd Microsoft.PowerShell.Core\FileSystem::\\wsl.localhost\<distro>\path\to\your\gvm-repo

python .\src\gvm\main.py --list

```

---

## Troubleshooting:

If you encounter an warning like this in vscode remote WSL2:

```plaintext
CMD.EXE was started with the above path as the current directory.
UNC paths are not supported.  Defaulting to Windows directory.
```

try mapping the WSL2 directory to a drive letter from windows cmd:

```cmd
net use X: \\wsl.localhost\Debian\your\projects\directory
```

then you can access the directory from vscode remote WSL2,
where `/mnt/x` is now mapped to your WSL2 projects directory.

```plaintext
/mnt/x/<this-repo-name>/src/gvm/main.py --list
```

and a launch configuration in vscode like:

```json
{
    "name": "Debug gvm/main.py --list",
    "type": "debugpy",
    "request": "launch",
    "program": "/mnt/x/gvm/src/gvm/main.py",
    "console": "integratedTerminal",
    "args": [
        "--list"
    ],
    "cwd": "/mnt/x/gvm",
    "env": {
        "PYTHONPATH": "/mnt/x/gvm/.venv/bin/python" // <- not yet sure if this does anything
    },
    "python": "${command:python.interpreterPath}", // <- not yet sure if this does anything
}
```

// ^^^ TODO: maybe there's a vscode builtin ${} for the repo root directory name?
