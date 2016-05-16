try:
    import lbtlib
except Exception:
    print("Unable to load lbtlib. Please redownload this program or download lbtlib from http://github.com/ZanyLeonic/LeonicBinaryTool")
    sys.exit(1)

print(lbtlib.iolib.downloadfile("http://zanyleonic.github.io/LeonicBinaryTool/version.ver", "h"))
