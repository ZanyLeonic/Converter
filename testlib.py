#!/usr/bin/python
import time
import os
import sys
import lbtlib

licenseabout="""
    Leonic Binary Tool
    Copyright (C) 2016 Leo Durrant
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """
t2btest="hello"
i2btest=255
wttftest="""
     Hello,
     this is a test file.
     meow neow
     hello world
    """
cwd=os.getcwd()
wttfname=cwd+"\\testtext.txt"
print(licenseabout)
print("")
print("Started testing at " + time.strftime("%H:%M:%S") + " on " + time.strftime("%d/%m/%Y") + ".")
print("")
print("Script current directory: " + os.getcwd())
print("Libraries in use:")
print(lbtlib.conlib.appname + " " + lbtlib.conlib.version + " " + lbtlib.conlib.release)
print(lbtlib.iolib.appname + " " + lbtlib.iolib.version + " " + lbtlib.iolib.release)
print("")
print("Testing " + lbtlib.conlib.appname + " functions")
print("Testing text2binary()...")
print("Trying to convert " + t2btest)
t2bres=lbtlib.conlib.text2binary(t2btest)
if t2bres == 1:
    print("Error occurred while using text2binary().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + t2btest + " to " + t2bres + ".")
print("")
print("Testing binary2text()...")
print("Trying to convert " + t2bres)
print("Attempting to convert binary back to string.")
b2tres=lbtlib.conlib.binary2text(t2bres)
if b2tres == 1:
    print("Error occurred while using binary2text().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + t2bres + " to " + b2tres + ".")
print("")
print("Testing int2binary()...")
print("Trying to convert " + str(i2btest))
i2bres=lbtlib.conlib.int2binary(i2btest)
if i2bres == 1:
    print("Error occurred while using int2binary().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + str(i2btest) + " to " + str(i2bres) + ".")
print("")
print("Testing binary2int()...")
print("Trying to convert " + i2bres)
b2ires=lbtlib.conlib.binary2int(i2bres)
if b2ires == 1:
    print("Error occurred while using binary2int().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + str(i2bres) + " to " + str(b2ires) + ".")
print("")
print("Finished testing conlib. All tests succeeded.")
print("")
print("Testing " + lbtlib.iolib.appname + " functions")
print("Testing writetotextfile()...")
print("Trying to write " + wttftest + " to " + wttfname)
wttfres=lbtlib.iolib.writetotextfile(wttftest, wttfname)
if wttfres == 1:
    print("Error occurred while using writetotextfile().")
    print("Please check iolib and check the code.")

print("writetotextfile() returned status " + str(wttfres))
print("")
print("Testing readfromtextfile()...")
print("Trying to read file " + wttfname)
rftf=lbtlib.iolib.readfromtextfile(wttfname)
if rftf == 1:
    print("Error occurred while using readfromtextfile().")
    print("Please check iolib and check the code.")
print ("readfromtextfile() returned " + str(rftf))
os.remove(wttfname)
print("Testing finished on iolib. All tests succeded.")
print("Finished testing lbtlib.")
print("Finished testing at " + time.strftime("%H:%M:%S") + " on " + time.strftime("%d/%m/%Y") + ".")
sys.exit(0)
