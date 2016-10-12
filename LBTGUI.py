# !/usr/bin/python3
try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter import filedialog
    import tkinter.scrolledtext as tkst
except Exception as e:
    print("Failed to import tkinter\n %s" % (str(e)))
    sys.exit(1)
    
try:
    from lbtlib import *
except Exception as e:
    messagebox.showerror("Fatal error", "Unable to load lbtlib. Please redownload this program or download lbtlib from http://github.com/ZanyLeonic/LeonicBinaryTool\n{}".format(str(e)))
    print("Unable to load lbtlib. Please redownload this program or download lbtlib from http://github.com/ZanyLeonic/LeonicBinaryTool\n{}".format(str(e)))
    sys.exit(1)

appname="Leonic Binary Tool"
author="Leo Durrant (2016)"
buliddate="10/10/16"
version="0.1a"
release="alpha"
progicon=r"resources\lbt.ico"
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

windowwidth=300
windowheight=250

def checkmethod(option, window):
    selected=str(option)
    
    if selected == "()":
        messagebox.showerror("Error", "Please select an option.")
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
    else:
        messagebox.showerror("Error", "{} is an invaild option, please try again.".format(selected))

def convert(mode, inputcon, window):
    converted=""
    window.destroy()

    if "0" in mode:
        try:
            print(inputcon)
            converted=conlib.text2binary(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            print("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "1" in mode:
        try:
            converted=conlib.binary2text(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            print("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "2" in mode:
        try:
            converted=conlib.int2binary(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            print("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    elif "3" in mode:
        try:
            converted=conlib.binary2int(inputcon)
            createresultwindow(mode, converted)
        except Exception as e:
            print("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, str(e)))
            messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s." % (inputcon, mode, str(e)))
    else:
        print("Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, "invaild operation."))
        messagebox.showerror("Error", "Error when converting %s to mode %s\n Exception: %s" % (inputcon, mode, "invaild operation."))
    
def showsettings():
    print("TODO: implement method.")

def showabout():
    print("TODO: implement method.")

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
        
def restart(window):
    window.destroy()
    createmainwindow()

def end(window):
    window.destroy()
    sys.exit(0)
    
def createmainwindow():
    windowwidth=300
    windowheight=250
    
    mainwindow = Tk()
    
    mainwindow.title(appname)
    try:
        mainwindow.iconbitmap(progicon)
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
    btn2 = Button(panel2, text="Settings", command=createsettingwindow, width=20)
    btn3 = Button(panel2, text="About", command=showabout, width=25)

    label1txt.set("Welcome to %s version %s.\n Please select an option below." % (appname, version))

    msb.insert(1, "Convert text to binary")
    msb.insert(2, "Convert binary to text")
    msb.insert(3, "Convert integer to binary")
    msb.insert(4, "Convert binary to integer")

    panel1.pack(side = TOP)
    label1.pack(side = TOP)
    msb.pack(side = TOP)
    btn1.pack(side = TOP)
    panel2.pack(side = TOP)
    btn2.pack(side = LEFT)
    btn3.pack(side = RIGHT)

    mainwindow.mainloop()

def createconvertwindow(mode):
    windowwidth=414
    windowheight=475
    
    convertwindow = Tk()
    modedesc = "null"
    
    if "0" in mode:
        modedesc="Convert text to binary"
    elif "1" in mode:
        modedesc="Convert binary to text"
    elif "2" in mode:
        modedesc="Convert integer to binary"
    elif "3" in mode:
        modedesc="Convert binary to integer"
    else:
        modedesc="Unknown or inproper implmented mode."
    txtcontent = ""
    filename = ""
    convertwindow.title("%s: %s" % (appname, modedesc))
    try:
        convertwindow.iconbitmap(progicon)
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

    convertwindow.mainloop()
    
def createresultwindow(mode, txt):
    windowwidth=414
    windowheight=530
    
    resultwindow = Tk()
    modedesc = "null"

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
    else:
        modedesc="Unknown or inproper implmented mode."
    
    resultwindow.title("%s: %s" % (appname, modedesc))
    try:
        resultwindow.iconbitmap(progicon)
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
    con1txt.set("Mode: {}\n The conversion has finished. Copy the text in the box below or click save.".format(modedesc))
    
    panel1.pack(side = TOP)
    con1.pack()
    conbox.pack(side = TOP)
    btn1.pack(side = TOP)
    btn2.pack(side = TOP)
    btn3.pack(side = TOP)
    btn4.pack(side = TOP)
	
    resultwindow.mainloop()

def createsettingwindow():
    windowwidth=300
    windowheight=250
    
    settingwindow = Tk()
    
    settingwindow.title(appname)
    try:
        settingwindow.iconbitmap(progicon)
    except Exception as e:
        messagebox.showerror("Error", "Error while setting program icon\n {}.".format(str(e)))
    settingwindow.geometry("{}x{}".format(windowwidth,windowheight))
    settingwindow.resizable(width=False, height=False)
    
createmainwindow()
