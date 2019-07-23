import sys, os
from cx_Freeze import setup, Executable
# https://stackoverflow.com/questions/50686243/cant-install-cx-freeze-or-scipy-for-python-3-7-64-bit

__version__ = "0.1"

include_files = ['config.txt']
#excludes = ['']
packages = ['os', 'sys', 'random', 'PySide2', 'wmi', 'subprocess', 'time', 'threading', 'pythoncom']

setup(
    name = "Auto Kill Disk",
    description = 'Automatic Drive Wipe Utility',
    version = __version__,
    options = {"build_exe": {
    #'packages': packages,
    #'include_files': include_files,
    #'excludes': excludes,
    'include_msvcr': True,
    }},
    executables = [Executable("autoKillDisk.py",base="Win32GUI")])