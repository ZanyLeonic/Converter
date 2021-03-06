#!/usr/bin/python3
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Console"

executableName = "Converter.exe"
executableIcon = "data\\images\\converter.ico"
includefiles = []
includes = []
excludes = ["tkinter"]
copyright = "(c) 2016 - 2017 Leo Durrant"
packages = ["convlib"]

options = {
    'build_exe': {
        'includes': includes,
        'excludes': excludes,
        'packages': packages,
        'include_files': includefiles,
    },
}

setup(
    name = "Converter",
    version = "0.21a",
    description = 'A small application that converts data to binary and hexadecimal - back and forth.',
    author = 'Leo Durrant',
    author_email = 'alexdrinka@outlook.com',
    options = options,
    executables = [Executable("Converter.py", base=base, targetName=executableName, icon=executableIcon, copyright=copyright,)]
)
