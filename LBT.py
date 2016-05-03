#!/usr/bin/python
import time
import os
import os.path
import sys
import webbrowser
import configparser
import logging
try:
    import lbtlib
except Exception:
    print("Unable to load lbtlib. Please redownload this program or download lbtlib from http://github.com/ZanyLeonic/LeonicBinaryTool")
    sys.exit(1)
                 
appname="Leonic Binary Tool"
version="0.1a"
release="alpha"
configfilename="config.ini"
configfilereadname=r"config.ini"
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
print(licenseabout)

loggingenabled=1
checkforupdatesonstartup=1
logger = logging.getLogger("[LBT]")
menu="null"

def readvaluefromconfig(section, valuename):
    try:
        config = configparser.ConfigParser()
        config.read(configfilereadname)
        try:
            val = config[section][valuename]
            return val
        except Exception:
            logger.error("Cannot find value " + valuename + " in " + section + ". Check " + configfilereadname + ".")
            print("Cannot find value " + valuename + " in " + section + ". Check " + configfilereadname + ".")
            return "null"
    except Exception:
        logger.error("Cannot read " + configfilereadname + ". Permission error or does the file not exist?")
        print("Error reading config. Check the log.")
        return "null"

def setvalueinconfig(section, key, value):
    config = configparser.ConfigParser()
    try:
        config.read(configfilereadname)
        config.set(section, key, value)
        with open(configfilename, 'w') as configfile:
            config.write(configfile)
    except Exception:
        logger.error("Unhandled error occurred while writing the config. Using default settings.")
        print("Unhandled error occurred while writing the config. Using default settings.")
            
def loadconfig():
    try:
        config = configparser.ConfigParser()
        config.read(configfilereadname)
        try:
            loggingenabled = readvaluefromconfig('general', 'createlog')
            if loggingenabled == "null":
                logging.info
                loggingenabled = 1
            checkforupdatesonstartup = readvaluefromconfig('updater', 'checkforupdatesonstartup')
        except Exception:
            loggingenabled = 1
            checkforupdatesonstartup = 1
            logger.error("Cannot find option value(s) in config.ini. Either the file doesn't exist or the value(s) are missing.")
            print("Config comprimised! Attempting to recreate...")
            createconfig()
    except Exception:
        print("Unknown exception. Trying to create config...")
        createconfig()

def createconfig():
    config = configparser.ConfigParser()
    config['general'] = {'createlog': '1'}
    config['updater'] = {'checkforupdatesonstartup': '1'}
    try:
        with open(configfilename, 'w') as configfile:
            config.write(configfile)
    except Exception:
        logger.error("Unhandled error occurred while writing the config. Using default settings.")
        print("Unhandled error occurred while writing the config. Using default settings.")
    
def setloggingoptions():
        logfilename = 'log.log'
        handler = logging.FileHandler(logfilename)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if loggingenabled == 0:
            logging.basicConfig()
        else:
            logging.basicConfig(filename=logfilename, level=logging.DEBUG)
        logger.addHandler(handler)
        logger.debug('Started %s at %s on %s', appname, time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"))

def about():
    aboutmenu = True
    while aboutmenu:
        print("============================================")
        print(appname)
        print("Version", version)
        print("Libraries in use:")
        print(lbtlib.conlib.appname + " " + lbtlib.conlib.version + " " + lbtlib.conlib.release)
        print(lbtlib.iolib.appname + " " + lbtlib.iolib.version + " " + lbtlib.iolib.release)
        print("This is release is an", release,"release.")
        print("Written by Leo Durrant on the 5/02/16.")
        print(licenseabout)
        print("============================================")
        print("""
        Please type the number of a function.
            1. Wordpress
            2. Github
            3. Back to main menu
        """)
        print("============================================")
        aboutmenu=input(">>> ")
        if aboutmenu == "1":
            webbrowser.open("http://leonicweb.wordpress.com/")
            print("Attempted to open 'http://leonicweb.wordpress.com/' in your default webbrowser.")
            print("If it failed to do so, enter the url in your browser.")
            aboutmenu = True
        elif aboutmenu == "2":
            webbrowser.open("http://github.com/ZanyLeonic/LeonicBinaryTool/")
            print("Attempted to open 'http://github.com/ZanyLeonic/LeonicBinaryTool/' in your default webbrowser.")
            print("If it failed to do so, enter the url in your browser.")
            aboutmenu = True
        elif aboutmenu == "3":
            aboutmenu = False
        else:
            print("Invalid selection.")
            mainmenusel = True

def converttext2binary():
    ct2b = True
    while ct2b:
        print("============================================")
        print("Welcome to", appname+"!")
        print("Version", version)
        print("Mode: Text to binary")
        print("============================================")
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        ct2b = input(">>> ")
        
        if ct2b == "1":
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            text=lbtlib.iolib.readfromtextfile(path)

            if text == 1:
                print("Cannot read " + path + ".")
                break
            else:
                convertedtext=lbtlib.conlib.text2binary(text)
                print("Your text file has been converted into binary and now reads:")
                print(convertedtext)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted binary as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedtext, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            ct2b=True
        elif ct2b == "2":
            print("Please input the text you want to converted into binary below.")
            text=input(">>> ")
            
            convertedtext=lbtlib.conlib.text2binary(text)
            print("Your text has been converted into binary and now reads:")
            print(convertedtext)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted binary as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedtext, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif ct2b == "3":
            ct2b = False

def convertbinary2text():
    cb2t = True
    while cb2t:
        print("============================================")
        print("Welcome to", appname+"!")
        print("Version", version)
        print("Mode: Binary to text")
        print("============================================")
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        cb2t = input(">>> ")
        
        if cb2t == "1":
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            binary=lbtlib.iolib.readfromtextfile(path)

            if binary == 1:
                print("Cannot read " + path + ".")
                break
            else:
                convertedbinary=lbtlib.conlib.binary2text(binary)
                print("Your text file has been converted into text and now reads:")
                print(convertedbinary)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted binary as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedtext, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            cb2t=True
        elif cb2t == "2":
            print("Please input the binary you want to converted into text below.")
            binary=input(">>> ")
            
            convertedtext=lbtlib.conlib.binary2text(binary)
            print("Your binary has been converted into text and now reads:")
            print(convertedtext)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted binary as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedtext, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif cb2t == "3":
            cb2t = False

def convertint2binary():
    ci2b = True
    while ci2b:
        print("============================================")
        print("Welcome to", appname+"!")
        print("Version", version)
        print("Mode: Integer to binary")
        print("============================================")
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        ci2b = input(">>> ")
        
        if ci2b == "1":
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            integer=lbtlib.iolib.readfromtextfile(path)

            if integer == 1:
                print("Cannot read " + path + ".")
                break
            else:
                convertedinteger=lbtlib.conlib.int2binary(integer)
                print("Your text file has been converted into text and now reads:")
                print(convertedinteger)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted binary as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedinteger, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            ci2b=True
        elif ci2b == "2":
            print("Please input the integer you want to converted into binary below.")
            integer=input(">>> ")
            
            convertedinteger=lbtlib.conlib.int2binary(integer)
            print("Your integer has been converted into binary and now reads:")
            print(convertedinteger)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted integer as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedinteger, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif ci2b == "3":
            ci2b = False

def convertbinary2int():
    cbti = True
    while cbti:
        print("============================================")
        print("Welcome to", appname+"!")
        print("Version", version)
        print("Mode: Binary to integer")
        print("============================================")
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        cbti = input(">>> ")
        
        if cbti == "1":
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            binary=lbtlib.iolib.readfromtextfile(path)
            if binary == 1:
                print("Cannot read " + path + ".")
                break
            else:
                convertedbinary=lbtlib.conlib.binary2int(binary)
                print("The binary inside your text file has been converted into an integer and now reads:")
                print(convertedbinary)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted binary as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedbinary, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            cbti=True
        elif cbti == "2":
            print("Please input the binary you want to converted into an integer below.")
            binary=input(">>> ")
            
            convertedbinary=lbtlib.conlib.binary2int(binary)
            print("Your binary has been converted into an integer and now reads:")
            print(convertedbinary)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted binary as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    lbtlib.iolib.writetotextfile(convertedbinary, path)
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif cbti == "3":
            cbti = False

def settings():
    catsets = True
    while catsets:
        print("============================================")
        print("Welcome to", appname+"!")
        print("Version", version)
        print("Settings")
        print("============================================")
        print("""
        Please type the number of a settings category.
            1. General
            2. Updater
            3. Back to main menu
        """)
        print("============================================")
        catsets = input(">>> ")
        
        if catsets == "1":
            sets1 = True
            while sets1:
                print("============================================")
                print("Welcome to", appname + "!")
                print("Version", version)
                print("Settings>General")
                print("============================================")
                print("""
                Please type the number of a setting to toggle or set.
                1. Logging """+ "(Current value: "+readvaluefromconfig("general", "createlog")+")"+"""
                2. Back to main menu
                """)
                print("============================================")
                sets1 = input(">>> ")
                if sets1 == "1":
                    currentlogval=readvaluefromconfig("general", "createlog")
                    if currentlogval=="1":
                        setvalueinconfig("general", "createlog", "0")
                    elif currentlogval=="0":
                        setvalueinconfig("general", "createlog", "1")
                elif sets1 == "2":
                    sets1 = False

        if catsets == "2":
            sets2 = True
            while sets2:
                print("============================================")
                print("Welcome to", appname + "!")
                print("Version", version)
                print("Settings>Updater")
                print("============================================")
                print("""
                Please type the number of a setting to toggle or set.
                1. Check for updates on startup """+ "(Current value: "+readvaluefromconfig("updater", "checkforupdatesonstartup")+")"+"""
                2. Back to main menu
                """)
                print("============================================")
                sets2 = input(">>> ")
                if sets2 == "1":
                    currentupostartval=readvaluefromconfig("updater", "checkforupdatesonstartup")
                    if currentupostartval=="1":
                        setvalueinconfig("updater", "checkforupdatesonstartup", "0")
                    elif currentupostartval=="0":
                        setvalueinconfig("updater", "checkforupdatesonstartup", "1")
                elif sets2 == "2":
                    sets2 = False

        if catsets == "3":
            catsets = False

def pathnotice():
    print("Please type the path where you wish to save the text file.")
    print("[WARNING]: Any existing file with the same name WILL BE OVERWRITTEN.")
    print("[TIP]: You can specifiy relative path from where the script is stored, but you can always put in a full path.")
                        
setloggingoptions()
loadconfig()
logger.info(appname + " loaded!")
logger.info("Version: " + version + " " + release)
menu="main"
mainmenusel = True
while mainmenusel:

    print("============================================")
    print("Welcome to", appname+"!")
    print("Version", version)
    print("============================================")
    print("""
    Please type the number of a function.
        1. Convert text to binary
        2. Convert binary to text
        3. Convert integer to binary
        4. Convert binary to integer
        5. Settings
        6. About
        7. Exit
    """)
    print("============================================")
    mainmenusel = input(">>> ")
    if mainmenusel == "1":
        logger.info("Chose option 1 on menu " + menu)
        converttext2binary()
        mainmenusel = True
    elif mainmenusel == "2":
        logger.info("Chose option 2 on menu " + menu)
        convertbinary2text()
        mainmenusel = True
    elif mainmenusel == "3":
        logger.info("Chose option 3 on menu " + menu)
        convertint2binary()
        mainmenusel = True
    elif mainmenusel == "4":
        logger.info("Chose option 4 on menu " + menu)
        convertbinary2int()
        mainmenusel = True
    elif mainmenusel == "5":
        logger.info("Chose option 5 on menu " + menu)
        settings()
        mainmenusel = True
    elif mainmenusel == "6":
        logger.info("Chose option 6 on menu " + menu)
        about()
        mainmenusel = True
    elif mainmenusel == "7":
        logger.info("Chose option 7 on menu " + menu)
        print("See ya!")
        logger.info("Exiting...")
        mainmenusel = False
    elif mainmenusel != "":
        print("Invalid selection.")
        mainmenusel = True
    else:
        print("Invalid selection.")
        mainmenusel = True
        
