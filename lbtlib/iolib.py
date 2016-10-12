import urllib.request

appname="LBT IO functions module"
author="Leo Durrant (2016)"
buliddate="12/10/16"
version="0.2a"
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

def writetotextfile(inputtext, paths):
    path=paths
    textfile = open(path, "w")
    textfile.write(inputtext)
    textfile.close()
        
def readfromtextfile(path):
    file=open(path,"r")
    text=file.read()
    return text

def readonlinefile(url):
        errorcode=1
        response = urllib.request.urlopen(url)
        errorcode=2
        data = response.read()
        errorcode=3
        text = data.decode('utf-8')
        errorcode=0
        text = str(text)
        return text

if __name__ == "__main__":
    print("%s by %s." % (appname, author))
    print("Version: %s %s built on %s" % (version, release, buliddate))
    print(licenseabout)
    print("""
    Available functions:
        writetotextfile(inputtext) - Writes inputtext to were the user specifies.
        readfromtextfile(path)     - Reads from the file specified in path.
        readonlinefile(url)        - Attempts to read the file specified in the URL returns text. If it fails, returns errorcode.
    For further releases and information check out the links below.""")
    print("""
    Wordpress: http://leonicweb.wordpress.com/
    Github: http://github.com/ZanyLeonic/LeonicBinaryTool/
    """)
    
