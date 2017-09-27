#!/usr/bin/python3
import time
import os
import sys
try:
    import convlib
except Exception:
    print("Unable to load convlib. Please redownload this program or download convlib from http://github.com/ZanyLeonic/LeonicBinaryTool")
    sys.exit(1)
    
version="0.1a"
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
def checkforupdates_test():
    onlineversioninfourl="http://zanyleonic.github.io/UpdateInfo/Converter/version.ver"
    latestversionurl="http://zanyleonic.github.io/UpdateInfo/Converter/latest.url"
    print("Checking for updates...")
    status=0
    try:
        onlineversion=convlib.iolib.readonlinefile(onlineversioninfourl)
        downloadurl=convlib.iolib.readonlinefile(latestversionurl)
    except:
        status=1
        print("Failed to check for updates. github.io is blocked or no internet connection?")
        sys.exit(1)
    if status == 0:
        print("Comparing onlineversion(%s) to local version(%s)." % (onlineversion, version))
        if not onlineversion==version:
            print("Version %s is avaiable for download. Would you like to get it now?" % (onlineversion))
            print("Test suceeded.")
        elif onlineversion==version:
            print("LBT is up to date!")
            print("LBT is up to date. Version (%s)" % (version))
            print("Test suceeded.")

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
print(convlib.conlib.appname + " " + convlib.conlib.version + " " + convlib.conlib.release)
print(convlib.iolib.appname + " " + convlib.iolib.version + " " + convlib.iolib.release)
print("")
print("Testing " + convlib.conlib.appname + " functions")
print("Testing text2binary()...")
print("Trying to convert " + t2btest)
t2bres=convlib.conlib.text2binary(t2btest)
if t2bres == 1:
    print("Error occurred while using text2binary().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + t2btest + " to " + t2bres + ".")
print("")
print("Testing binary2text()...")
print("Trying to convert " + t2bres)
print("Attempting to convert binary back to string.")
b2tres=convlib.conlib.binary2text(t2bres)
if b2tres == 1:
    print("Error occurred while using binary2text().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + t2bres + " to " + b2tres + ".")
print("")
print("Testing int2binary()...")
print("Trying to convert " + str(i2btest))
i2bres=convlib.conlib.int2binary(i2btest)
if i2bres == 1:
    print("Error occurred while using int2binary().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + str(i2btest) + " to " + str(i2bres) + ".")
print("")
print("Testing binary2int()...")
print("Trying to convert " + i2bres)
b2ires=convlib.conlib.binary2int(i2bres)
if b2ires == 1:
    print("Error occurred while using binary2int().")
    print("Please check conlib and check the code.")
    sys.exit(1)
print("Ok, converted " + str(i2bres) + " to " + str(b2ires) + ".")
print("")
print("Finished testing conlib. All tests succeeded.")
print("")
print("Testing " + convlib.iolib.appname + " functions")
print("Testing writetotextfile()...")
print("Trying to write " + wttftest + " to " + wttfname)
wttfres=convlib.iolib.writetotextfile(wttftest, wttfname)
if wttfres == 1:
    print("Error occurred while using writetotextfile().")
    print("Please check iolib and check the code.")

print("writetotextfile() returned status " + str(wttfres))
print("")
print("Testing readfromtextfile()...")
print("Trying to read file " + wttfname)
rftf=convlib.iolib.readfromtextfile(wttfname)
if rftf == 1:
    print("Error occurred while using readfromtextfile().")
    print("Please check iolib and check the code.")
print ("readfromtextfile() returned " + str(rftf))
os.remove(wttfname)
print("Testing readonlinetextfile()...")
checkforupdates_test()
print("Testing finished on iolib. All tests succeded.")
print("Finished testing convlib.")
print("Finished testing at " + time.strftime("%H:%M:%S") + " on " + time.strftime("%d/%m/%Y") + ".")
sys.exit(0)
