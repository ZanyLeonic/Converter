appname="LBT Conversion module"
author="Leo Durrant (2016)"
buliddate="03/05/16"
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

def text2binary(inputtext):
    try:
        bits = bin(int.from_bytes(inputtext.encode(encoding='utf-8', errors='surrogatepass'), 'big'))[2:]
        return bits.zfill(8 * ((len(bits) + 7) // 8))
    except:
        print("Failed to convert the text (%s) to binary." % (inputtext))
        return 1

def binary2text(inputbin):
    try:
        n = int(inputbin, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding='utf-8', errors='surrogatepass') or '\0'
    except:
        print("Failed to convert the binary (%s) to text." % (inputbin))
        return 1

def int2binary(inputint):
    try:
        num = int(inputint)
        output = '{0:08b}'.format(num)
        return output
    except:
        print("Failed to parse the input as a integer (%s). Please make sure your number is a whole number and doesn't have anything else, except numbers." % (inputint))
        return 1

def binary2int(inputbin):
    try:
        integer = int(inputbin, 2)
        return integer
    except:
        print("Failed to convert binary (%s) to integer!" % (inputbin))
        return 1

if __name__ == "__main__":
    print("%s by %s." % (appname, author))
    print("Version: %s %s built on %s" % (version, release, buliddate))
    print(licenseabout)
    print("""
    Available functions:
        text2binary(inputtext) - Converts inputtext into binary and returns it.
        binary2text(inputbin)  - Converts inputbin into a string and returns it.
        int2binary(inputint)   - Converts inputint into binary and returns it.
        binary2int(inputbin)   - Converts inputbin into an integer and returns it.
    For further releases and information check out the links below.""")
    print("""
    Wordpress: http://leonicweb.wordpress.com/
    Github: http://github.com/ZanyLeonic/LeonicBinaryTool/
    """)
    
