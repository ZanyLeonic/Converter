#!/usr/bin/python3
try:
    import time
    import os
    import os.path
    import sys
    import platform
    import webbrowser
    import configparser
    import logging
except Exception as e:
    print("Failed to import standard Python libraries.\n Please check your Python version and install.\n Exception: %s" % (str(e)))
    
try:
    import PIL.Image
except Exception as e:
    print("Failed to import Python Image Library\n Please install it with pip using 'pip install pillow'. (Shouldn't be a much of a problem.) \n Exception: %s" % (str(e)))
    
try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import filedialog
    from tkinter import PhotoImage
    import tkinter.scrolledtext as tkst
except Exception as e:
    print("Failed to import tkinter\n %s" % (str(e)))
    sys.exit(1)
    
try:
    from lbtlib import *
except Exception as e:
    messagebox.showerror("Fatal error", "Unable to load lbtlib. Please redownload this program or download lbtlib from http://github.com/ZanyLeonic/LeonicBinaryTool\nException: {}".format(str(e)))
    print("Unable to load lbtlib. Please redownload this program or download lbtlib from http://github.com/ZanyLeonic/LeonicBinaryTool\nException: {}".format(str(e)))
    sys.exit(1)

# App info
appname="Converter"
author="Leo Durrant (2016/17)"
buliddate="10/10/16"
version="0.2a"
release="alpha"

# App resources
configfilename="data//config_gui.ini"
configfilereadname=r"data/config_gui.ini"
progicon=r"data/images/converter.ico"
abouticon=r"data/images/about_con.gif"

# Some import error thingys

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
# Standard window settings
windowwidth=300
windowheight=250

# App settings and variables
loggingenabled=1
checkforupdatesonstartup=1
onlineversioninfourl="http://zanyleonic.github.io/Converter/version.ver"
latestversionurl="http://zanyleonic.github.io/Converter/latest.url"
websiteurl="http://leonic.no-ip.biz/"
githuburl="http://github.com/ZanyLeonic/Converter/"
patchnotesurl="http://zanyleonic.github.io/Converter/latest.info"
logger=logging.getLogger("[Converter]")
conversionsaved=0
currentdir=os.path.dirname(os.path.realpath(__file__))
systemos=iolib.systemos()
patchnotesopen=False

def checkmethod(option, window):
    selected=str(option)
    
    if selected == "()":
        messagebox.showerror("Error", "Please select an option.")
        logger.error("User chose option {}. But {} is an invaild option!".format(selected, selected))
    elif "0" in selected:
        window.destroy();
        createconvertwindow(selected)
    elif "1" in selected:
        window.destroy();
        createconvertwindow(selected)
    elif "2" in selected:
        window.destroy();
        createconvertwindow(selected)
    elif "3" in selected:
        window.destroy();
        createconvertwindow(selected)
    elif "4" in selected:
        window.destroy();
        createconvertwindow(selected)
    elif "5" in selected:
        messagebox.showinfo("Information", "Every seperate hexadecimal has to be on a new line in order to be converted correctly.")
        window.destroy();
        createconvertwindow(selected)
    else:
        logger.error("User chose option {}. But {} is an invaild option!".format(selected, selected))
        messagebox.showerror("Error", "{} is an invaild option, please try again.".format(selected))
        
def empty():
    print("", end="")
    
def convert(mode, inputcon, window):
    converted=""
    window.destroy()

    if "0" in mode:
        try:
            print(inputcon)
            converted=conlib.text2binary(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            logger.error("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "1" in mode:
        try:
            converted=conlib.binary2text(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            logger.error("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "2" in mode:
        try:
            converted=conlib.int2binary(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            logger.error("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "3" in mode:
        try:
            converted=conlib.binary2int(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            logger.error("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "4" in mode:
        try:
            converted=conlib.text2hexdec(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            logger.error("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "5" in mode:
        try:
            inputcon=inputcon.strip()
            converted=conlib.hexdec2text(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            logger.error("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    else:
        logger.error("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
        messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, "invaild operation."))
    
def showsettings(window):
    logger.info("Opening settings window from window")
    window.destroy()
    createsettingwindow()

def showabout():
    logger.info("Opening about window from window")
    createaboutwindow()
    
def initializesetting(section, valuename, checkbutton):
    value=False
    try:
        value=int(readvaluefromconfig(section, valuename))
    except Exception as e:
        logger.error("Invaild value '%s' from section '%s'.\n Exception: %s" % (valuename, section, str(e)))
        messagebox.showerror("Error", "Invaild value '%s' from section '%s'.\n Exception: %s" % (valuename, section, str(e)))

    if value == 1:
        checkbutton.select()
    elif value == 0:
        checkbutton.deselect()
    else:
        logger.error("Invaild value '%s' from section '%s'." % (valuename, section))
        messagebox.showerror("Error", "Invaild value '%s' from section '%s'." % (valuename, section))
        
def readvaluefromconfig(section, valuename):
    try:
        config = configparser.ConfigParser()
        config.read(configfilereadname)
        try:
            val = config[section][valuename]
            return val
        except Exception as e:
            logger.error("Cannot find value %s in %s. Check %s.\n Exception: %s\n Attempting to create..." % (valuename, section, configfilereadname, str(e)))
            messagebox.showerror("Error", "Cannot find value %s in %s. Check %s.\n Exception: %s\n Attempting to create..." % (valuename, section, configfilereadname, str(e)))
            createconfig()
            return "null"
    except Exception as e:
        logger.error("Cannot read %s.\n Exception: %s" % (configfilereadname, str(e)))
        messagebox.showerror("Error", "Cannot read %s.\n Exception: %s" % (configfilereadname, str(e)))
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
        messagebox.showerror("Error", "Unhandled error occurred while writing the config. Using default settings.\n Exception: %s" % (str(e)))
            
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
        except Exception as e:
            loggingenabled = 1
            checkforupdatesonstartup = 1
            logger.error("Cannot find option value(s) in config.ini.\n Exception: %s" % (str(e)))
            print("Configuration file out of date! Rebuilding...")
            createconfig()
    except Exception as e:
        createconfig()

def createconfig():
    config = configparser.ConfigParser()
    config['general'] = {'createlog': '1'}
    config['updater'] = {'checkforupdatesonstartup': '1'}
    try:
        with open(configfilename, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        logger.error("Unhandled error occurred while writing the config. Using default settings.\n Exception: %s" % (str(e)))
        messagebox.showerror("Error", "Unhandled error occurred while writing the config. Using default settings.\n Exception: %s" % (str(e)))
    
def setloggingoptions():
    while True:
        try:
            logfilename = 'data//logs//log_gui ({}).log'.format(time.strftime("%d-%m-%Y"))
            handler = logging.FileHandler(logfilename)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            if loggingenabled == 0:
                logging.basicConfig()
            else:
                logging.basicConfig(filename=logfilename, level=logging.DEBUG)
            logger.addHandler(handler)
            logger.handlers.pop()
            logger.debug('Started %s at %s on %s', appname, time.strftime("%H:%M:%S"), time.strftime("%d/%m/%Y"))
            logger.info('Running on {} version {}.'.format(platform.system(), platform.release()))
            logger.info("%s version (%s %s) started in directory: %s", appname, version, release, currentdir)
            break
        except Exception as e:
            messagebox.showerror("Error", "Cannot create log.\n Exception: %s\nTrying to create logs folder..." % (str(e)))
            try:
                os.mkdir("data//logs")
            except Exception as e:
                messagebox.showerror("Error", "Cannot create logs folder.\n Exception: %s" % (str(e)))

def savefile(master, text):
    try:
        filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),
                                                         ("All files", "*.*") ))
        if not filename == "":
            txtcontent = iolib.writetotextfile(text, filename)
            if txtcontent == 1:
                print("Something went wrong while saving : %s.\n Does this user have to approrite permissions to the file?" % (filename))
                messagebox.showerror("Error", "Something went wrong while saving to: %s.\n Do you have the approrite permissions to the file?" % (filename))
            else:
                conversionsaved=1
                print("Saved conversion to %s." % (filename))
                messagebox.showinfo("Saved", "Saved conversion to %s." % (filename))
                # print(txtcontent) # debugging purposes.
        else:
            # print("passed") # debugging purposes.
            pass
    except Exception as e:
        print("Error while loading file picker.\n %s." % (str(e)))
        messagebox.showerror("Error", "Error while loading file save.\n %s." % (str(e)))
        filename = 1
    return filename

def openfile(master, textbox):
    try:
        filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),
                                                         ("All files", "*.*") ))
        if not filename == "":
            txtcontent = iolib.readfromtextfile(filename)
            if txtcontent == 3:
                print("Something went wrong while reading: %s.\n Does this user have to approrite permissions to the file?" % (filename))
                messagebox.showerror("Error", "Something went wrong while reading: %s.\n Do you have to approrite permissions to the file?" % (filename))
            else:
                textbox.insert(INSERT, txtcontent)
                # print(txtcontent) # debugging purposes.
        else:
            # print("passed") # debugging purposes.
            pass
    except Exception as e:
        print("Error while loading file picker.\n %s." % (str(e)))
        messagebox.showerror("Error", "Error while loading file picker.\n %s." % (str(e)))
        filename = 1
    return filename

def copytoclipboard(window, content):
    try:
        window.clipboard_clear()
        window.clipboard_append(content)
        messagebox.showinfo("Success", "Content copied to clipboard.")
    except Exception as e:
        print("Failed to copy '%s' to the clipboard.\n Exception: %s" % (content, str(e)))
        messagebox.showerror("Error", "Failed to copy '%s' to the clipboard.\n Exception: %s." % (content, str(e)))

def exittowindow(window, nextwindow=0):
    window.destroy()
    if nextwindow == 0:
        createmainwindow()

def exitapp(window):
    window.destroy()
    sys.exit(0)

def checkforupdates(supressinfo=True):
    status=0
    try:
        print("Checking for updates...", end=" ")
        onlineversion=iolib.readonlinefile(onlineversioninfourl)
        downloadurl=iolib.readonlinefile(latestversionurl)
        patchnotes=iolib.readonlinefile(patchnotesurl)
    except Exception as e:
        print("Failed!")
        status=1
        logger.error("Failed to check for updates.\n Exception: %s" % (str(e)))
        if supressinfo == False:
            messagebox.showerror("Check for updates", "Failed to check for updates.\n Exception: {}".format(str(e)), icon='info')

    if status == 0:
        logger.info("Comparing onlineversion(%s) to local version(%s)." % (onlineversion, version))
        if not onlineversion==version:
            logger.info("Version %s is avaiable." % (onlineversion))
            createupdateinfowindow("Version {} is available".format(onlineversion), patchnotes, onlineversion, downloadurl)
        elif onlineversion==version:
            if supressinfo == False:
                messagebox.showinfo("Check for updates", "{} is up to date at version {}.".format(appname, version))
            logger.info("%s is up to date. Version (%s)" % (appname, version))

def restart(window):
    window.destroy()
    createmainwindow()

def end(window):
    window.destroy()
    sys.exit(0)

def closepatchnotes(window):
    global patchnotesopen
    patchnotesopen=False
    window.destroy()

def closewindowandopenurl(window, downloadurl):
    window.destroy()
    webbrowser.open(downloadurl)

def createupdateinfowindow(title, text, onversion, downloadurl):
    
    if systemos == 0:
        windowwidth=385
        windowheight=93
    elif systemos == 1:
        windowwidth=385
        windowheight=93
    else:
        windowwidth=385
        windowheight=93
    abouticon1=r"data/images/about_con.gif"
    licensewindow = Toplevel()
    licensewindow.title("{}: {}".format(appname, title))
    try:
      if systemos == 0: # Check if the user is using Windows...
          licensewindow.iconbitmap(progicon)
      else: # If not...
          ico = PhotoImage(file=abouticon1)
          licensewindow.tk.call('wm', 'iconphoto', licensewindow._w, ico)
    except Exception as e:
        messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
    licensewindow.geometry("{}x{}".format(windowwidth,windowheight))

    choicebox = Frame(licensewindow)
    updatelabel = Label(licensewindow, text="Version {} is available.\nDo you want to download it now? (Current version: {})".format(onversion, version))
    
    btn1 = Button(choicebox, text="Patch notes", command=lambda: createlicensewindow("Patch notes (Version {})".format(onversion), text, True))
    btn2 = Button(choicebox, text="Yes", command=lambda: closewindowandopenurl(licensewindow, downloadurl))
    btn3 = Button(choicebox, text="No", command=lambda: licensewindow.destroy())

    btn1.grid(row=0, column=3, sticky=N+S+W+E, padx=2, pady=5)
    btn2.grid(row=0, column=1, sticky=N+S+W+E, padx=2, pady=5)
    btn3.grid(row=0, column=2, sticky=N+S+W+E, padx=2, pady=5)

    choicebox.pack(side=BOTTOM)
    updatelabel.pack()
    
def createlicensewindow(title, text, patchnotes=False):
    global patchnotesopen
    
    if systemos == 0:
        windowwidth=670
        windowheight=375
    elif systemos == 1:
        windowwidth=670
        windowheight=350
    else:
        windowwidth=670
        windowheight=350
    abouticon1=r"data/images/about_con.gif"
    licensewindow = Toplevel()
    licensewindow.title("{}: {}".format(appname, title))
    if patchnotesopen==True:
        licensewindow.destroy()
    else: 
        try:
          if systemos == 0: # Check if the user is using Windows...
              licensewindow.iconbitmap(progicon)
          else: # If not...
              ico = PhotoImage(file=abouticon1)
              licensewindow.tk.call('wm', 'iconphoto', licensewindow._w, ico)
        except Exception as e:
            messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
        licensewindow.geometry("{}x{}".format(windowwidth,windowheight))

    if patchnotes == True:
        if patchnotesopen==False:
            patchnotesopen=True
            licensewindow.protocol("WM_DELETE_WINDOW", lambda: closepatchnotes(licensewindow))
    
    aboutbox = tkst.ScrolledText(licensewindow, width=str(windowwidth), height=str(windowheight))

    aboutbox.insert(INSERT, text)
    
    aboutbox.pack(side = TOP)
    
    aboutbox.mainloop()

def createmainwindow():
    windowwidth=300
    windowheight=250
    
    mainwindow = Toplevel()
    
    mainwindow.title(appname)
    try:
      if systemos == 0: # Check if the user is using Windows...
          mainwindow.iconbitmap(progicon)
      else: # If not...
          ico = PhotoImage(file=abouticon)
          mainwindow.tk.call('wm', 'iconphoto', mainwindow._w, ico)
    except Exception as e:
        messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
    mainwindow.geometry("{}x{}".format(windowwidth,windowheight))
    mainwindow.resizable(width=False, height=False)

    panel1 = Frame(mainwindow)
    panel2 = Frame(mainwindow)

    label1txt = StringVar()
    label1 = Label(panel1, textvariable=label1txt, relief=SUNKEN, width=str(windowwidth))
    msb = Listbox(panel1, width=str(windowwidth))
    btn1 = Button(mainwindow, text="Continue", command=lambda: checkmethod(msb.curselection(), mainwindow), width=str(windowwidth))
    btn2 = Button(panel2, text="Settings", command=lambda: showsettings(mainwindow), width=20)
    btn3 = Button(panel2, text="About", command=showabout, width=25)

    label1txt.set("Welcome to %s version %s.\n Please select an option below." % (appname, version))

    msb.insert(1, "Convert text to binary")
    msb.insert(2, "Convert binary to text")
    msb.insert(3, "Convert integer to binary")
    msb.insert(4, "Convert binary to integer")
    msb.insert(5, "Convert text and integer to hexadecimal")
    msb.insert(6, "Convert hexadecminal to text and integer")

    panel1.pack(side = TOP)
    label1.pack(side = TOP)
    msb.pack(side = TOP)
    btn1.pack(side = TOP)
    panel2.pack(side = TOP)
    btn2.pack(side = LEFT)
    btn3.pack(side = RIGHT)

    mainwindow.protocol("WM_DELETE_WINDOW", lambda: exitapp(mainwindow))
    mainwindow.mainloop()

def createconvertwindow(mode):
    windowwidth=414
    windowheight=475
    
    convertwindow = Toplevel()
    modedesc = "null"
    
    if "0" in mode:
        modedesc="Convert text to binary"
    elif "1" in mode:
        modedesc="Convert binary to text"
    elif "2" in mode:
        modedesc="Convert integer to binary"
    elif "3" in mode:
        modedesc="Convert binary to integer"
    elif "4" in mode:
        modedesc="Convert text and integer to hexadecimal"
    elif "5" in mode:
        modedesc="Convert hexadecimal to text and integer"
    else:
        modedesc="Unknown or inproper implmented mode."
    txtcontent = ""
    filename = ""
    convertwindow.title("%s: %s" % (appname, modedesc))
    try:
      if systemos == 0:
          convertwindow.iconbitmap(progicon)
      else:
          ico = PhotoImage(file=abouticon)
          convertwindow.tk.call('wm', 'iconphoto', convertwindow._w, ico)
    except Exception as e:
      messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
    convertwindow.geometry("{}x{}".format(windowwidth,windowheight))
    convertwindow.resizable(width=False, height=False)

    panel1 = Frame(convertwindow)
    panel2 = Frame(convertwindow)

    con1txt = StringVar()
    con1 = Label(panel1, textvariable=con1txt, relief=SUNKEN, width=str(windowwidth))
    conbox = tkst.ScrolledText(panel1, width=str(windowwidth))
    btn1 = Button(convertwindow, text="Continue", command=lambda: convert(mode, conbox.get("1.0", END), convertwindow), width=str(windowwidth))
    btn2 = Button(convertwindow, text="Browse...", command=lambda: openfile(convertwindow, conbox), width=str(windowwidth))

    con1txt.set("Mode: {}\n Select a text file or type some into the textbox.".format(modedesc))
    
    panel1.pack(side = TOP)
    con1.pack()
    conbox.pack(side = TOP)
    btn1.pack(side = TOP)
    panel2.pack(side = TOP)
    btn2.pack(side = BOTTOM)

    convertwindow.protocol("WM_DELETE_WINDOW", lambda: exittowindow(convertwindow))
    convertwindow.mainloop()

def createresultwindow(mode, txt):
    windowwidth=414
    windowheight=530
    
    resultwindow = Toplevel()
    modedesc = "null"
    conversionsaved=0
    
    txtcontent = ""
    filename = ""

    if "0" in mode:
        modedesc="Convert text to binary"
    elif "1" in mode:
        modedesc="Convert binary to text"
    elif "2" in mode:
        modedesc="Convert integer to binary"
    elif "3" in mode:
        modedesc="Convert binary to integer"
    elif "4" in mode:
        modedesc="Convert text and integer to hexadecimal"
    elif "5" in mode:
        modedesc="Convert hexadecimal to text and integer"
    else:
        modedesc="Unknown or inproper implmented mode."
    
    resultwindow.title("%s: %s" % (appname, modedesc))
    try:
      if systemos == 0:
          resultwindow.iconbitmap(progicon)
      else:
          ico = PhotoImage(file=abouticon)
          resultwindow.tk.call('wm', 'iconphoto', resultwindow._w, ico)
    except Exception as e:
        messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
    resultwindow.geometry("{}x{}".format(windowwidth, windowheight))
    resultwindow.resizable(width=False, height=False)

    panel1 = Frame(resultwindow)

    con1txt = StringVar()
    con1 = Label(panel1, textvariable=con1txt, relief=SUNKEN, width=str(windowwidth))
    conbox = tkst.ScrolledText(panel1, width=str(windowwidth))
    btn1 = Button(resultwindow, text="Convert again", command=lambda: restart(resultwindow), width=str(windowwidth))
    btn2 = Button(resultwindow, text="Copy to clipboard", command=lambda: copytoclipboard(resultwindow, conbox.get("1.0", END)), width=str(windowwidth))
    btn3 = Button(resultwindow, text="Save", command=lambda: savefile(resultwindow, conbox.get("1.0", END)), width=str(windowwidth))
    btn4 = Button(resultwindow, text="Quit", command=lambda: end(resultwindow), width=str(windowwidth))

    conbox.insert(INSERT, txt)
    con1txt.set("Mode: {}\n The conversion has finished. Copy the text in the box below\n or click save.".format(modedesc))
    
    panel1.pack(side = TOP)
    con1.pack()
    conbox.pack(side = TOP)
    btn1.pack(side = TOP)
    btn2.pack(side = TOP)
    btn3.pack(side = TOP)
    btn4.pack(side = TOP)
    
    resultwindow.protocol("WM_DELETE_WINDOW", lambda: exittowindow(resultwindow))
    resultwindow.mainloop()

def createsettingwindow():
    windowwidth=300
    windowheight=250
    
    settingwindow = Toplevel()
    
    settingwindow.title("{}: Settings".format(appname))
    try:
      if systemos == 0:
          settingwindow.iconbitmap(progicon)
      else:
          ico = PhotoImage(file=abouticon)
          settingwindow.tk.call('wm', 'iconphoto', settingwindow._w, ico)
    except Exception as e:
        messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
    settingwindow.geometry("{}x{}".format(windowwidth,windowheight))
    settingwindow.resizable(width=False, height=False)

    panel1 = Frame(settingwindow)
    panel2 = Frame(settingwindow)

    group1 = LabelFrame(settingwindow, text="General", padx=5, pady=5)
    group2 = LabelFrame(settingwindow, text="Updater", padx=5, pady=5)

    con1txt = StringVar()
    con2txt = StringVar()

    check1val = IntVar()
    check2val = IntVar()
    
    con1txt.set("Modify the settings below to change\n the way the program works.")
    con2txt.set("* These settings require {} to be\n restarted for full effect.".format(appname))
    
    checkbox1 = Checkbutton(group1, text="Create log*",  variable=check1val, width=str(windowwidth), command=lambda: setvalueinconfig("general", "createlog", str(check1val.get())))
    checkbox2 = Checkbutton(group2, text="Check for updates on startup",  variable=check2val, width=str(windowwidth), command=lambda: setvalueinconfig("updater", "checkforupdatesonstartup", str(check2val.get())))

    btn1 = Button(panel2, text="Close", command=lambda: restart(settingwindow), width=str(windowwidth))
    
    con1 = Label(panel1, textvariable=con1txt, relief=SUNKEN, width=str(windowwidth))
    con2 = Label(panel2, textvariable=con2txt, width=str(windowwidth))
    
    initializesetting("general","createlog", checkbox1)
    initializesetting("updater","checkforupdatesonstartup", checkbox2)
    
    panel1.pack(side=TOP)
    group1.pack(side=TOP, padx=10, pady=10)
    group2.pack(side=TOP, padx=10, pady=10)
    panel2.pack(side=BOTTOM)

    con1.pack()
    con2.pack()
    checkbox1.pack(side=LEFT)
    checkbox2.pack(side=LEFT)
    btn1.pack(side=BOTTOM)

    settingwindow.protocol("WM_DELETE_WINDOW", empty)
    settingwindow.mainloop()

def createaboutwindow():

    if systemos == 0:
        windowwidth=475
        windowheight=350
    elif systemos == 1:
        windowwidth=625
        windowheight=350
    else:
        windowwidth=625
        windowheight=350

    aboutwindow = Toplevel()
    
    aboutwindow.title("{}: About".format(appname))
    try:
      if systemos == 0:
          aboutwindow.iconbitmap(progicon)
      else:
          ico = PhotoImage(file=abouticon)
          aboutwindow.tk.call('wm', 'iconphoto', aboutwindow._w, ico)
    except Exception as e:
        messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
    aboutwindow.geometry("{}x{}".format(windowwidth,windowheight))
    aboutwindow.resizable(width=False, height=False)

    try:
        opensourcetext=iolib.readfromtextfile("data/text/opensourcelibraries.txt")
        legalinfotext=iolib.readfromtextfile("data/text/legalinfo.txt")
    except:
        print("error lol")
    
    panel1=Frame(aboutwindow, padx=5, pady=5, width=str(windowwidth))
    links=LabelFrame(aboutwindow, padx=5, pady=5, width=str(windowwidth), height=10, text="")
    
    lbt_logo= PhotoImage(file=abouticon)
    logolabel=Label(panel1, image=lbt_logo, text="")
    
    about_name=Label(panel1, text=appname)
    about_license=Label(panel1, text="This product '{}' , '{}'\n and '{}' are all under the GPLv3 license.\nClick the 'Legal info' button below for more infomation.".format(appname, conlib.appname, iolib.appname)) 
    about_verinfo=Label(panel1, text="Version: {} ({})".format(version, release), width=str(windowwidth))
    about_appbuildinfo=Label(panel1, text="Written by {} on the {}".format(author, buliddate))
    about_conlib=Label(panel1, text="{} {} ({}) by {}. \nBuilt on {}.".format(conlib.appname, conlib.version, conlib.release, conlib.author, conlib.buliddate), width=str(windowwidth))
    about_iolib=Label(panel1, text="{} {} ({}) by {}. \nBuilt on {}.".format(iolib.appname, iolib.version, iolib.release, iolib.author, iolib.buliddate), width=str(windowwidth))
    about_extrainfo=Label(panel1, text="Please report any bugs to the issues tracker on the\n Github repo and tell me what I can improve on this app.\n All feedback apperciated!", width=str(windowwidth))

    btn1=Button(links, text="Legal info", command=lambda: createlicensewindow("Legal info", legalinfotext))
    btn2=Button(links, text="Github", command=lambda: iolib.openinwebbrowser(githuburl))
    btn3=Button(links, text="Website", command=lambda: iolib.openinwebbrowser(websiteurl))
    btn4=Button(links, text="Check for updates", command=lambda: checkforupdates(False))
    btn5=Button(links, text="Help", command=empty)
    btn6=Button(links, text="Open source libraries", command=lambda: createlicensewindow("Open source", opensourcetext))
    
    panel1.pack(padx=20, pady=5)
    links.pack(padx=5, pady=5, side=BOTTOM)
    
    logolabel.pack()
    about_name.pack()
    about_verinfo.pack()
    about_license.pack()
    about_appbuildinfo.pack()
    about_conlib.pack()
    about_iolib.pack()
    about_extrainfo.pack()

    btn1.pack(side=LEFT, padx=1)
    btn2.pack(side=LEFT, padx=1)
    btn3.pack(side=LEFT, padx=1)
    btn4.pack(side=LEFT, padx=1)
    btn5.pack(side=LEFT, padx=1)
    btn6.pack(side=LEFT, padx=1)
    
    aboutwindow.mainloop()
    
print("Starting...")

# Main window for messageboxes.
root = Tk()
root.title("{}".format(appname))
try:
    if systemos == 0:
        root.iconbitmap(progicon)
    else:
        ico = PhotoImage(file=abouticon)
        root.tk.call('wm', 'iconphoto', root._w, ico)
except Exception as e:
    root.withdraw()
    messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))

root.withdraw()

setloggingoptions()
loadconfig()
checkforupdates()
createmainwindow()
