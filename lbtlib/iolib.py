appname="Leonic's IO functions module"
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

def writetotextfile(inputtext):
    print("Please type the path where you wish to save the text file.")
    print("[WARNING]: Any existing file with the same name WILL BE OVERWRITTEN.")
    print("[TIP]: You can specifiy realtive paths from where the script is stored, but you can always put in a full path.")
    path=input(">>> ")

    try:
        textfile = open(path, "w")
        textfile.write(inputtext)
        textfile.close()
    except:
        print("Failed to write to", path, ". Please try a different location.")
    print("Finished writing to", path,".")

def readfromtextfile(path):
    try:
        file=open(path,"r")
        text=file.read()
        return text
    except:
        print("Failed to open ", path,". Please check if the file exists.")
        return ""

if __name__ == "__main__":
    print(appname)
    print("Version: " + version + " " + release)
    print(licenseabout)
    print("""
    Available functions:
        writetotextfile(inputtext) - Writes inputtext to were the user specifies.
        readfromtextfile(path)     - Reads from the file specified in path.
    For further releases and information check out the links below.""")
    print("""
    Wordpress: http://leonicweb.wordpress.com/
    Github: http://github.com/ZanyLeonic/LeonicBinaryTool/
    """)
    
