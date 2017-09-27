#!/usr/bin/python3
import time
import os
import os.path
import sys
import webbrowser
import configparser
import logging
import platform
try:
    import convlib
except Exception:
    print("Unable to load convlib. Please redownload this program or download convlib from http://github.com/ZanyLeonic/Converter")
    sys.exit(1)
                 
appname="Converter"
author="Leo Durrant (2016/17)"
buliddate="27/09/17"
version="0.21a"
release="alpha"
configfilename="data//config_cmd.ini"
configfilereadname=r"data/config_cmd.ini"
licenseabout="""
    Converter
    Copyright (C) 2016, 2017 Leo Durrant

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
print("Starting...")
print(licenseabout)

bLoggingEnabled=1
bCheckforupdatesonstartup=1
bAppendtxtwhensaving=1
onlineversioninfourl="http://zanyleonic.github.io/UpdateInfo/Converter/version.ver"
latestversionurl="http://zanyleonic.github.io/UpdateInfo/Converter/latest.url"
logger=logging.getLogger("[Converter]")
menu="null"
menudisplayname="null"
appfrozen=False

# Check if the app is frozen
if getattr(sys, 'frozen', False):
    appfrozen = True

if appfrozen == True and convlib.iolib.isexe64bit() == True:
    onlineversioninfourl="http://zanyleonic.github.io/UpdateInfo/Converter/win64/version.ver"
    latestversionurl="http://zanyleonic.github.io/UpdateInfo/Converter/win64/latest.url"
    patchnotesurl="http://zanyleonic.github.io/UpdateInfo/Converter/win64/latest.info"
elif appfrozen == True and convlib.iolib.isexe64bit() == False:
    onlineversioninfourl="http://zanyleonic.github.io/UpdateInfo/Converter/win32/version.ver"
    latestversionurl="http://zanyleonic.github.io/UpdateInfo/Converter/win32/latest.url"
    patchnotesurl="http://zanyleonic.github.io/UpdateInfo/Converter/win32/latest.info"

#cx_freeze
if appfrozen == True:
    # Using cx_freeze
    currentdir=os.path.dirname(sys.executable)
else:
    # Running as a script.
    currentdir=os.path.dirname(os.path.realpath(__file__))

systemos=convlib.iolib.systemos()

def menutitle(menudisplayname):
        print("============================================")
        print("Welcome to %s!" % (appname))
        print("Version %s" % (version))
        print("Mode: %s" % (menudisplayname))
        print("============================================")

try:
    config = configparser.ConfigParser()
    config.read(configfilereadname)
except Exception as e:
        logger.error("Cannot read %s.\n Exception: %s" % (configfilereadname, str(e)))
        print("Cannot read %s.\n Exception: %s" % (configfilereadname, str(e)))

def readvaluefromconfig(section, valuename):
    try:
        config = configparser.ConfigParser()
        config.read(configfilereadname)
        try:
            val = config[section][valuename]
            return val
        except Exception as e:
            logger.error("Cannot find value %s in %s. Check %s.\n Exception: %s" % (valuename, section, configfilereadname, str(e)))
            print("Cannot find value %s in %s. Check %s.\n Exception: %s" % (valuename, section, configfilereadname, str(e)))
            return "null"
    except Exception as e:
        logger.error("Cannot read %s.\n Exception: %s" % (configfilereadname, str(e)))
        print("Cannot read %s.\n Exception: %s" % (configfilereadname, str(e)))
        return "null"

def setvalueinconfig(section, key, value):
    config = configparser.ConfigParser()
    try:
        config.read(configfilereadname)
        config.set(section, key, value)
        with open(configfilename, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        logger.error("Unhandled error occurred while writing the config. Using default settings.\n Exception: %s" % (str(e)))
        print("Unhandled error occurred while writing the config. Using default settings.\n Exception: %s" % (str(e)))
            
def loadconfig():
    if os.path.exists(configfilereadname) == True:
        try:
            config = configparser.ConfigParser()
            config.read(configfilereadname)
            try:
                bLoggingEnabled = readvaluefromconfig('general', 'bLoggingEnabled')
                if bLoggingEnabled == "null":
                    logging.info
                    bLoggingEnabled = 1
                bCheckforupdatesonstartup = readvaluefromconfig('updater', 'bCheckforupdatesonstartup')
            except Exception as e:
                bLoggingEnabled = 1
                bCheckforupdatesonstartup = 1
                logger.error("Cannot find option value(s) in config.ini.\n Exception: %s" % (str(e)))
                print("Config compromised! Attempting to recreate...")
                createconfig()
        except Exception as e:
            print("Trying to create config...\n Exception: %s" % (str(e)))
            createconfig()
    else:
        createconfig()

def createconfig():
    config = configparser.ConfigParser()
    config['general'] = {'bLoggingEnabled': '1', 'bAppendtxtwhensaving': '1'}
    config['updater'] = {'bCheckforupdatesonstartup': '1'}
    try:
        with open(configfilename, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        logger.error("Unhandled error occurred while writing the config. Using default settings.\n Exception: %s" % (str(e)))
        print("Unhandled error occurred while writing the config. Using default settings.\n Exception: %s" % (str(e)))
    
def setloggingoptions():
    while True:
        if os.path.exists("data//logs") == True:
            try:
                logfilename = 'data//logs//log_cmd ({}).log'.format(time.strftime("%d-%m-%Y"))
                handler = logging.FileHandler(logfilename)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                if bLoggingEnabled == 0:
                    logging.basicConfig()
                else:
                    logging.basicConfig(filename=logfilename, level=logging.DEBUG)
                logger.addHandler(handler)
                logger.handlers.pop()
                logger.debug('Started %s at %s on %s', appname, time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"))
                logger.info('Running on {} version {}.'.format(platform.system(), platform.release()))
                # cx_freeze?
                if appfrozen == True:
                    logger.info("Currently running the frozen version. Compiled by cx_freeze.")
                else:
                    logger.info("Currently running from the Python script.")
                logger.info("%s version (%s %s) started in directory: %s", appname, version, release, currentdir)
                break
            except Exception as e:
                print("Cannot create log. \n Exception: %s\nTrying to create logs folder..." % (str(e)))
                try:
                    os.mkdir("data//logs")
                except Exception as e:
                    print("Cannot create logs folder.\n Exception: %s" % (str(e)))

        else:
            os.mkdir("data//logs")
def checkforupdates():
    menu="update"
    print("Checking for updates...")
    status=0
    try:
        onlineversion=convlib.iolib.readonlinefile(onlineversioninfourl)
        downloadurl=convlib.iolib.readonlinefile(latestversionurl)
    except Exception as e:
        status=1
        print("Failed to check for updates.\n Exception: %s" % (str(e)))
        logger.error("Failed to check for updates.\n Exception: %s" % (str(e)))

    if status == 0:
        logger.info("Comparing onlineversion(%s) to local version(%s)." % (onlineversion, version))
        if not onlineversion==version:
            print("Version %s is avaiable for download. Would you like to get it now? (Y/N)" % (onlineversion))
            logger.info("Version %s is avaiable." % (onlineversion))
            update=True
            while update==True:
                update=input(">>> ")
                if update=="Y" or update=="y":
                    logger.info("Chose option (%s) on menu (%s)" % (update, menu))
                    print("Opening in default webbrowser...")
                    webbrowser.open(downloadurl)
                    update=False
                elif update=="N" or update=="n":
                    logger.info("Chose option (%s) on menu (%s)" % (update, menu))
                    print("")
                    update=False
                else:
                    logger.info("Chose option (%s) on menu (%s)" % (update, menu))
                    print("Invalid option.")
                    update=True
        elif onlineversion==version:
            print("Converter is up to date!")
            logger.info("Converter is up to date. Version (%s)" % (version))

def getenvdesc():
    # Initialize the variable...
    appflavourinfo=""

    # Then decide what it is going to hold.
    if appfrozen == True and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 0:
        appflavourinfo="a 64-bit executable on Windows."
    elif appfrozen == True and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 0:
        appflavourinfo="a 32-bit executable on Windows."
    elif appfrozen == False and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 0:
        appflavourinfo="a script running on a 64-bit interpreter on Windows."
    elif appfrozen == False and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 0:
        appflavourinfo="a script running on a 32-bit interpreter on Windows."
    elif appfrozen == True and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 1:
        appflavourinfo="a 64-bit executable on Linux."
    elif appfrozen == True and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 1:
        appflavourinfo="a 32-bit executable on Linux."
    elif appfrozen == False and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 1:
        appflavourinfo="a script running on a 64-bit interpreter on Linux."
    elif appfrozen == False and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 1:
        appflavourinfo="a script running on a 32-bit interpreter on Linux."
    elif appfrozen == True and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 2:
        appflavourinfo="a 64-bit executable on MacOS."
    elif appfrozen == True and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 2:
        appflavourinfo="a 32-bit executable on MacOS."
    elif appfrozen == False and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 2:
        appflavourinfo="a script running on a 64-bit interpreter on MacOS."
    elif appfrozen == False and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 2:
        appflavourinfo="a script running on a 32-bit interpreter on MacOS."
    elif appfrozen == True and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 3:
        appflavourinfo="a 64-bit executable on Unknown."
    elif appfrozen == True and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 3:
        appflavourinfo="a 32-bit executable on Unknown."
    elif appfrozen == False and convlib.iolib.isexe64bit() == True and convlib.iolib.systemos() == 3:
        appflavourinfo="a script running on a 64-bit interpreter on Unknown."
    elif appfrozen == False and convlib.iolib.isexe64bit() == False and convlib.iolib.systemos() == 3:
        appflavourinfo="a script running on a 32-bit interpreter on Unknown."
    else:
        appflavourinfo="an Unknown mode on an Unknown OS."
    
    return appflavourinfo

def about():
    aboutmenu = True
    while aboutmenu:
        menu="about"
        print("============================================")
        print(appname)
        print("Version %s" % (version))
        print("Running as %s" % (getenvdesc()))
        print("Libraries in use:")
        print("%s %s %s by %s. Built on %s." % (convlib.conlib.appname, convlib.conlib.version, convlib.conlib.release, convlib.conlib.author, convlib.conlib.buliddate))
        print("%s %s %s by %s. Built on %s." % (convlib.iolib.appname, convlib.iolib.version, convlib.iolib.release, convlib.iolib.author, convlib.iolib.buliddate))
        print("This release is an %s release." % (release))
        print("Written by %s on the %s." % (author, buliddate))
        print(licenseabout)
        print("============================================")
        print("""
        Please type the number of a function.
            1. Website
            2. Github
            3. Check for updates
            4. Back to main menu
        """)
        print("============================================")
        aboutmenu=input(">>> ")
        if aboutmenu == "1":
            logger.info("Chose option (%s) on menu (%s)" % (aboutmenu, menu))
            webbrowser.open("http://leonic.no-ip.biz/")
            print("Attempted to open 'http://leonic.no-ip.biz/' in your default webbrowser.")
            print("If it failed to do so, enter the url into your browser.")
            aboutmenu = True
        elif aboutmenu == "2":
            logger.info("Chose option (%s) on menu (%s)" % (aboutmenu, menu))
            webbrowser.open("http://github.com/ZanyLeonic/Converter/")
            print("Attempted to open 'http://github.com/ZanyLeonic/Converter/' in your default webbrowser.")
            print("If it failed to do so, enter the url into your browser.")
            aboutmenu = True
        elif aboutmenu == "3":
            logger.info("Chose option (%s) on menu (%s)" % (aboutmenu, menu))
            checkforupdates()
            aboutmenu = True
        elif aboutmenu == "4":
            logger.info("Chose option (%s) on menu (%s)" % (aboutmenu, menu))
            aboutmenu = False
        else:
            logger.info("Chose option (%s) on menu (%s)" % (aboutmenu, menu))
            print("Invalid selection.")
            mainmenusel = True

def converttext2binary():
    ct2b = True
    while ct2b:
        menu="ct2b"
        menudisplayname="Convert text to binary"
        menutitle(menudisplayname)
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        ct2b = input(">>> ")
        
        if ct2b == "1":
            logger.info("Chose option (%s) on menu (%s)" % (ct2b, menu))
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            try:
                text=convlib.iolib.readfromtextfile(path)
            except Exception as e:
                print("Cannot read %s.\n Exception: %s" % (path, str(e)))
                break
            try:
                convertedtext=convlib.conlib.text2binary(text)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (text, str(e)))
                break

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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedtext, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            ct2b=True
        elif ct2b == "2":
            logger.info("Chose option (%s) on menu (%s)" % (ct2b, menu))
            print("Please input the text you want to converted into binary below.")
            text=input(">>> ")
            try:
                convertedtext=convlib.conlib.text2binary(text)
            except Exception as e:
                print("Cannot converted %s.\n Exception: %s" % (text, str(e)))
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedtext, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                        
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif ct2b == "3":
            logger.info("Chose option (%s) on menu (%s)" % (ct2b, menu))
            ct2b = False

        else:
            logger.info("Chose option (%s) on menu (%s)" % (ct2b, menu))
            print("Invalid option.")
            ct2b=True

def convertbinary2text():
    cb2t = True
    while cb2t:
        menu="cb2t"
        menudisplayname="Convert binary to text"
        menutitle(menudisplayname)
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        cb2t = input(">>> ")
        
        if cb2t == "1":
            logger.info("Chose option (%s) on menu (%s)" % (cb2t, menu))
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            try:
                binary=convlib.iolib.readfromtextfile(path)
            except Exception as e:
                print("Cannot read %s.\n Exception: %s" % (path, str(e)))
                break
            try:
                convertedbinary=convlib.conlib.binary2text(binary)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (binary, str(e)))
                break
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedtext, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            cb2t=True
        elif cb2t == "2":
            logger.info("Chose option (%s) on menu (%s)" % (cb2t, menu))
            print("Please input the binary you want to converted into text below.")
            binary=input(">>> ")
            try:
                convertedtext=convlib.conlib.binary2text(binary)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (binary, str(e)))
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedtext, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif cb2t == "3":
            logger.info("Chose option (%s) on menu (%s)" % (cb2t, menu))
            cb2t = False

        else:
            logger.info("Chose option (%s) on menu (%s)" % (cb2t, menu))
            print("Invalid option.")
            cb2t=True
def convertint2binary():
    ci2b = True
    while ci2b:
        menu="ci2b"
        menudisplayname="Convert integer to binary"
        menutitle(menudisplayname)
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        ci2b = input(">>> ")
        
        if ci2b == "1":
            logger.info("Chose option (%s) on menu (%s)" % (ci2b, menu))
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            try:
                integer=convlib.iolib.readfromtextfile(path)
            except Exception as e:
                print("Cannot read %s.\n Exception: %s" % (path, str(e)))
                break
            try:
                convertedinteger=convlib.conlib.int2binary(integer)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (integer, str(e)))
                break
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedinteger, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            ci2b=True
        elif ci2b == "2":
            logger.info("Chose option (%s) on menu (%s)" % (ci2b, menu))
            print("Please input the integer you want to converted into binary below.")
            integer=input(">>> ")
            try:
                convertedinteger=convlib.conlib.int2binary(integer)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (integer, str(e)))
                break
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedinteger, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif ci2b == "3":
            logger.info("Chose option (%s) on menu (%s)" % (ci2b, menu))
            ci2b = False

        else:
            logger.info("Chose option (%s) on menu (%s)" % (ci2b, menu))
            print("Invalid option.")
            ci2b=True
            
def convertbinary2int():
    cbti = True
    while cbti:
        menu="cb2i"
        menudisplayname="Convert binary to integer"
        menutitle(menudisplayname)
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        cbti = input(">>> ")
        
        if cbti == "1":
            logger.info("Chose option (%s) on menu (%s)" % (cbti, menu))
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            try:
                binary=convlib.iolib.readfromtextfile(path)
            except Exception as e:
                print("Cannot read %s.\n Exception: %s" % (path, str(e)))
                break
            try:
                convertedbinary=convlib.conlib.binary2int(binary)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (binary, str(e)))
                break
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedbinary, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            cbti=True
        elif cbti == "2":
            logger.info("Chose option (%s) on menu (%s)" % (cbti, menu))
            print("Please input the binary you want to converted into an integer below.")
            binary=input(">>> ")
            try:
                convertedbinary=convlib.conlib.binary2int(binary)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (binary, str(e)))
                break
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedbinary, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif cbti == "3":
            logger.info("Chose option (%s) on menu (%s)" % (cbti, menu))
            cbti = False

        else:
            logger.info("Chose option (%s) on menu (%s)" % (cbti, menu))
            print("Invalid option.")
            cbti=True
            
def converttextinttohex():
    ctith = True
    while ctith:
        menu="ctith"
        menudisplayname="Convert text and integer to hexadecimal"
        menutitle(menudisplayname)
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        ctith = input(">>> ")
        
        if ctith == "1":
            logger.info("Chose option (%s) on menu (%s)" % (ctith, menu))
            print("Please enter a path to the text file you wish to convert.")
            path=input(">>> ")
            try:
                txtint=convlib.iolib.readfromtextfile(path)
            except Exception as e:
                print("Cannot read %s.\n Exception: %s" % (path, str(e)))
                break
            try:
                convertedtext=convlib.conlib.text2hexdec(txtint)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (binary, str(e)))
                break
            print("The text inside your text file has been converted into hexadecimal and now reads:")
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
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedtext, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            ctith=True
        elif ctith == "2":
            logger.info("Chose option (%s) on menu (%s)" % (ctith, menu))
            print("Please input the binary you want to converted into an integer below.")
            text=input(">>> ")
            try:
                convertedtext=convlib.conlib.text2hexdec(text)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (text, str(e)))
                break
            print("Your binary has been converted into an integer and now reads:")
            print(convertedtext)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted text as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedtext, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif ctith == "3":
            logger.info("Chose option (%s) on menu (%s)" % (ctith, menu))
            cbti = False

        else:
            logger.info("Chose option (%s) on menu (%s)" % (ctith, menu))
            print("Invalid option.")
            cbti=True

def converthextotextint():
    chtti = True
    while chtti:
        menu="chtti"
        menudisplayname="Convert hexadecimal to text/int"
        menutitle(menudisplayname)
        print("""
        Please type the number of a function.
            1. Open a text file to convert
            2. Type text to convert
            3. Back to main menu
        """)
        print("============================================")
        chtti = input(">>> ")
        
        if chtti == "1":
            logger.info("Chose option (%s) on menu (%s)" % (chtti, menu))
            print("Please enter a path to the text file you wish to convert.")
            print("Note: Make sure each hex is on a different line in order for the hex to be converted correctly.")
            path=input(">>> ")
            try:
                hexin=convlib.iolib.readfromtextfile(path)
            except Exception as e:
                print("Cannot read %s.\n Exception: %s" % (path, str(e)))
                break
            try:
                convertedhex=convlib.conlib.hexdec2text(hexin)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (binary, str(e)))
                break
            print("The hexadecimal inside your text file has been converted and now reads:")
            print(convertedhex)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted hexadecimal as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedhex, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
                    
            chtti=True
        elif chtti == "2":
            logger.info("Chose option (%s) on menu (%s)" % (chtti, menu))
            print("Please input the hexadecimal you want to converted below.")
            print("Note: At the moment only one hex can be converted at a time using this method.")
            print("Note: Use a text file to convert the hex or the GUI version to avoid this.")
            hexin=input(">>> ")
            try:
                convertedhex=convlib.conlib.hexdec2text(hexin)
            except Exception as e:
                print("Cannot convert %s.\n Exception: %s" % (hexin, str(e)))
                break
            print("Your binary has been converted into an integer and now reads:")
            print(convertedhex)
            
            writetotextfilemenu=True
            while writetotextfilemenu:
                print("Do you want to save the converted text as a text file?")
                print("1. Yes")
                print("2. No")
                writetotextfilemenu=input(">>> ")

                if writetotextfilemenu == "1":
                    pathnotice()
                    path=input(">>> ")
                    try:
                        if bAppendtxtwhensaving == 1:
                            path = path + ".txt"
                        convlib.iolib.writetotextfile(convertedhex, path)
                    except Exception as e:
                        print("Cannot write %s.\n Exception: %s" % (path, str(e)))
                    writetotextfilemenu=False

                elif writetotextfilemenu == "2":
                    writetotextfilemenu=False

                else:
                    print("Invalid selection")
                    writetotextfilemenu=True
            
        elif chtti == "3":
            logger.info("Chose option (%s) on menu (%s)" % (chtti, menu))
            chtti = False

        else:
            logger.info("Chose option (%s) on menu (%s)" % (chtti, menu))
            print("Invalid option.")
            chtti=True
            
def settings():
    catsets = True
    while catsets:
        menu="settings"
        print("============================================")
        print("Welcome to %s!" %(appname))
        print("Version %s" %(version))
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
            logger.info("Chose option (%s) on menu (%s)" % (catsets, menu))
            sets1 = True
            while sets1:
                menu="settings>general"
                bLoggingEnabledcurval=readvaluefromconfig("general", "bLoggingEnabled")
                bAppendtxtwhensavingcurval=readvaluefromconfig("general", "bAppendtxtwhensaving")
                print("============================================")
                print("Welcome to %s!" %(appname))
                print("Version %s" % (version))
                print("Settings>General")
                print("============================================")
                print("""
         Please type the number of a setting to toggle or set.
            1. Logging (Current value: %s)
            2. Append '.txt' when saving (Current value: %s)
            3. Back to main menu
                """ % (bLoggingEnabledcurval, bAppendtxtwhensavingcurval))
                print("============================================")
                sets1 = input(">>> ")
                if sets1 == "1":
                    logger.info("Chose option (%s) on menu (%s)" % (sets1, menu))
                    currentlogval=readvaluefromconfig("general", "bLoggingEnabled")
                    if currentlogval=="1":
                        setvalueinconfig("general", "bLoggingEnabled", "0")
                    elif currentlogval=="0":
                        setvalueinconfig("general", "bLoggingEnabled", "1")
                elif sets1 == "2":
                    logger.info("Chose option (%s) on menu (%s)" % (sets1, menu))
                    currentappendtxtval=readvaluefromconfig("general", "bAppendtxtwhensaving")
                    if currentappendtxtval=="1":
                        setvalueinconfig("general", "bAppendtxtwhensaving", "0")
                    elif currentappendtxtval=="0":
                        setvalueinconfig("general", "bAppendtxtwhensaving", "1")
                elif sets1 == "3":
                    logger.info("Chose option (%s) on menu (%s)" % (sets1, menu))
                    sets1 = False

        elif catsets == "2":
            logger.info("Chose option (%s) on menu (%s)" % (catsets, menu))
            sets2 = True
            while sets2:
                menu="settings>updater"
                updatercurval=readvaluefromconfig("updater", "bCheckforupdatesonstartup")
                print("============================================")
                print("Welcome to %s!" % (appname))
                print("Version %s" % (version))
                print("Settings>Updater")
                print("============================================")
                print("""
        Please type the number of a setting to toggle or set.
            1. Check for updates on startup (Current value: %s)
            2. Back to main menu
                """ % (updatercurval))
                print("============================================")
                sets2 = input(">>> ")
                if sets2 == "1":
                    logger.info("Chose option (%s) on menu (%s)" % (sets2, menu))
                    currentupostartval=readvaluefromconfig("updater", "bCheckforupdatesonstartup")
                    if currentupostartval=="1":
                        setvalueinconfig("updater", "bCheckforupdatesonstartup", "0")
                    elif currentupostartval=="0":
                        setvalueinconfig("updater", "bCheckforupdatesonstartup", "1")
                elif sets2 == "2":
                    logger.info("Chose option (%s) on menu (%s)" % (sets2, menu))
                    sets2 = False

        elif catsets == "3":
            logger.info("Chose option (%s) on menu (%s)" % (catsets, menu))
            catsets = False

        else:
            logger.info("Chose option (%s) on menu (%s)" % (catsets, menu))
            print("Invalid option.")
            catsets=True

def pathnotice():
    print("Please type the path where you wish to save the text file.")
    print("[WARNING]: Any existing file with the same name WILL BE OVERWRITTEN.")
    print("[TIP]: You can specifiy relative path from where the script is stored, but you can always put in a full path.")
                        
setloggingoptions()
loadconfig()

logger.info("%s loaded!" % (appname))
logger.info("Version: %s %s" % (version,release))

menu="main"
mainmenusel = True
while mainmenusel:

    print("============================================")
    print("Welcome to %s!" % (appname))
    print("Version %s" % (version))
    print("============================================")
    print("""
    Please type the number of a function.
        1. Convert text to binary
        2. Convert binary to text
        3. Convert integer to binary
        4. Convert binary to integer
        5. Convert text/int to hexadecimal
        6. Convert hexadecimal to text/int
        7. Settings
        8. About
        9. Exit
    """)
    print("============================================")
    mainmenusel = input(">>> ")
    if mainmenusel == "1":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        converttext2binary()
        mainmenusel = True
    elif mainmenusel == "2":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        convertbinary2text()
        mainmenusel = True
    elif mainmenusel == "3":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        convertint2binary()
        mainmenusel = True
    elif mainmenusel == "4":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        convertbinary2int()
        mainmenusel = True
    elif mainmenusel == "5":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        converttextinttohex()
        mainmenusel = True
    elif mainmenusel == "6":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        converthextotextint()
        mainmenusel = True
    elif mainmenusel == "7":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        settings()
        mainmenusel = True
    elif mainmenusel == "8":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        about()
        mainmenusel = True
    elif mainmenusel == "9":
        logger.info("Chose option (%s) on menu (%s)" % (mainmenusel, menu))
        print("See ya!")
        logger.info("Exiting...")
        mainmenusel = False
    elif mainmenusel != "":
        print("Invalid selection.")
        mainmenusel = True
    else:
        print("Invalid selection.")
        mainmenusel = True
