#!/usr/bin/python3
# Remember to copy the tk and tcl dll files to the build folder after building!
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executableName = "ConverterGUI.exe"
executableIcon = "data\\images\\converter.ico"
includefiles = []
includes = []
excludes = []
copyright = "(c) 2016 - 2017 Leo Durrant"
packages = ["tkinter", "convlib"]

options = {
    'build_exe': {
        'includes': includes,
        'excludes': excludes,
        'packages': packages,
        'include_files': includefiles,
    },
}

setup(
    name = "Converter (GUI)",
    version = "0.21a",
    description = 'A small application that converts data to binary and hexadecimal - back and forth.',
    author = 'Leo Durrant',
    author_email = 'alexdrinka@outlook.com',
    options = options,
    executables = [Executable("ConverterGUI.py", base=base, targetName=executableName, icon=executableIcon, copyright=copyright,)]
)
