#!/usr/bin/python
import time
import os
import os.path
import sys
import webbrowser
import configparser
import logging
appname="Leonic ETC functions module"
version="0.1a"
release="alpha"
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
def createeula(workingdir):
    eula=workingdir+"\\eula.txt"
    config = configparser.ConfigParser()
    config['main'] = {'eula': 'false'}
    #try:
    with open(eula, 'w') as configfile:
        config.write(eula)
   #except Exception:
        #print("Unhandled error occurred while writing the eula. Exiting...")
        #sys.exit(1)

def checkeula(workingdir):
    try:
        config = configparser.ConfigParser()
        config.read(workingdir + "\\eula.txt")
        try:
            eula = config["main"]["eula"]
            return eula
        except Exception:
            print("Cannot find eula value " + valuename + " in " + section + ". Check " + workingdir + "\\eula.txt" + ".")
            return "null"
    except Exception:
        print("Error reading eula. Check the log.")
        return "null"

def seteula(value, workingdir):
    config = configparser.ConfigParser()
    try:
        config.read(workingdir + "\\eula.txt")
        config.set("main", "eula", value)
        with open(configfilename, 'w') as configfile:
            config.write(configfile)
    except Exception:
        print("Failed to change the EULA value!")

if __name__ == "__main__":
    print(appname)
    print("Version: " + version + " " + release)
    print(licenseabout)
    print("""
    Available functions:
        createeula(workingdir) - Creates the eula file relative from the workingdir.
        checkeula(workingdir)  - Checks the eula file relative from the workindir.
		seteula(value, workingdir) - Sets the eula in the specified directory.
    For further releases and information check out the links below.""")
    print("""
    Wordpress: http://leonicweb.wordpress.com/
    Github: http://github.com/ZanyLeonic/LeonicBinaryTool/
    """)
    
