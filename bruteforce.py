import sys, getopt
import zlib
from hash40 import Hash40

chars = "abcdefghijklmnopqrstuvwxyz_0123456789"
prefix = ''
suffix = ''
length = 0
checkAll = False
ignoreNum = False
hashes = []
defaultPath = "hashes.txt"

def getInputLength():
    global prefix, suffix
    return len(prefix) + len(suffix)

def openFile(path):
    global hashes
    tag = None
    f = open(path, "r")
    for x in f:
        if(x != "\n"):
            if x[0] == '-':
                tag = x[1:].strip()
            else:
                hashes.append(Hash40(x.lower().strip(), tag))

def doCRC(string):
    h = hex(zlib.crc32(bytearray(string, 'utf-8')))
    if len(h.replace("0x","")) < 8:
        h = "0x" + ('0' * (8 - len(h.replace("0x","")))) + h.replace("0x","")
    return h

def check(string):
    global prefix, suffix
    hash = doCRC(prefix + string + suffix)
    length = len(prefix + string + suffix)
    find = next((x for x in hashes if hash == x.hash and length == x.length), None)
    if find:
        if find.tag is None:
            print("{0} -> {1}".format(find.hash40, prefix + string + suffix))
        else:
            print("{2} {0} -> {1}".format(find.hash40, prefix + string + suffix, find.tag))

def process(string):
    global length, checkAll
    if(checkAll):
        check(string)
        if(len(string) + getInputLength() < length):
            loop(string)
    else:
        if(len(string) + getInputLength() == length):
            check(string)
        else:
            if(len(string)  + getInputLength() < length):
                loop(string)

def loop(string):
    global chars
    for char in chars:
        process(string + char)

#Prints first character to show progress
def StartLoop():
    global chars
    for char in chars:
        print(char)
        process(char)

def start(argv):
    global defaultPath, prefix, suffix, length, checkAll, chars, ignoreNum
    path = defaultPath
    try:
      opts, args = getopt.getopt(argv,"hl:p:s:f",["suffix=","prefix=","length=", "checkAll", "file=", "ignoreNum"])
    except getopt.GetoptError:
        print('Usage: bruteforce.py -l <int> (-p <string>) (-s <string>) (--checkAll)')
        print('bruteforce.py -h for help')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('bruteforce.py -l <int> (-p <string>) (-s <string>) (--checkAll)')
            print("-l/--length= <int>: Max length of strings, takes into account prefix and suffix. If checkAll isn't enabled only strings with this length will be hashed and compared with list")
            print("-p/--prefix= <string>: Prefix to add to generated strings")
            print("-s/--suffix= <string>: Suffix to add to generated strings")
            print("--checkAll: Check all strings hashes regardless of length")
            sys.exit()
        elif opt in ("--prefix", "-p"):
            prefix = arg
        elif opt in ("--sufix", "-s"):
            suffix = arg
        elif opt in ("--length", "-l"):
            length = int(arg)
        elif opt in ("--checkAll"):
            checkAll = True
        elif opt in ("--ignoreNum"):
            ignoreNum = True
        elif opt in ("--file", "-f"):
            path = arg
    
    if(length == 0):
        print("Error: No length given")
        print('Usage: bruteforce.py -l <int> (-p <string>) (-s <string>) (--checkAll)')
        sys.exit()

    if(ignoreNum):
        chars = "abcdefghijklmnopqrstuvwxyz_"
    openFile(path)
    if(getInputLength() < length):
        StartLoop()
    else:
        print("length is lower than prefix + suffix")

if __name__ == "__main__":
    start(sys.argv[1:])