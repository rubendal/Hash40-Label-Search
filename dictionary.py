import sys, getopt
import zlib
from hash40 import Hash40

dictionary = []
prefix = ''
suffix = ''
length = 0
depth = 0
checkAll = False
hashes = []
defaultPath = "hashes.txt"
dictionaryPath = "dictionary.txt"

def getInputLength():
    global prefix, suffix
    return len(prefix) + len(suffix)

def openDict():
    global dictionary, dictionaryPath
    f = open(dictionaryPath, "r")
    for x in f:
        dictionary.append(x.lower().strip())

def openFile(path):
    global hashes
    f = open(path, "r")
    for x in f:
        if(x != "\n"):
            hashes.append(Hash40(x.lower().strip()))

def doCRC(string):
    return hex(zlib.crc32(bytearray(string, 'utf-8')))

def check(string):
    global prefix, suffix
    hash = doCRC(prefix + string + suffix)
    length = len(prefix + string + suffix)
    find = next((x for x in hashes if hash == x.hash and length == x.length), None)
    if find:
        print("{0} -> {1}".format(find.hash40, prefix + string + suffix))

def checkLoop(currentDepth, prevWords, prevWord, string):
    global depth
    if(depth == 0):
        loop(currentDepth, prevWords, prevWord, string)
    else:
        if(currentDepth < depth):
            loop(currentDepth, prevWords, prevWord, string)

def process(currentDepth, prevWords, prevWord, string):
    global length, checkAll
    if(checkAll):
        if(len(string) + getInputLength() < length):
            check(string)
            checkLoop(currentDepth + 1, prevWords, prevWord, string)
    else:
        if(len(string) + getInputLength() == length):
            check(string)
        else:
            if(len(string)  + getInputLength() < length):
                checkLoop(currentDepth + 1, prevWords, prevWord, string)

def loop(currentDepth, prevWords, prevWord, string):
    global dictionary
    for word in dictionary:
        if(word not in prevWords):
            if(prevWord != "_" and word != "_"):
                words = prevWords.copy()
                if(word != "_"):
                    words.append(word)
                process(currentDepth, words, word, string + "_" + word)

#Prints first character to show progress
def StartLoop():
    global dictionary
    for word in dictionary:
        print(word)
        process(0, [word], word, word)

def start(argv):
    global defaultPath, prefix, suffix, length, checkAll, depth
    path = defaultPath
    try:
      opts, args = getopt.getopt(argv,"hl:d:p:s:f",["suffix=","prefix=","length=", "checkAll", "file=", "depth="])
    except getopt.GetoptError:
        print('dictionary.py -l <int> (-d <int>) (-p <string>) (-s <string>) (--checkAll)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dictionary.py -l <int> (-p <string>) (-s <string>) (--checkAll)')
            print("-l/--length= <int>: Max length of strings, takes into account prefix and suffix. If checkAll isn't enabled only strings with this length will be hashed and compared with list")
            print("-d/--depth= <int>: Max amount of words to use (prefix/suffix not counted)")
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
        elif opt in ("--depth", "-d"):
            depth = int(arg)
        elif opt in ("--checkAll"):
            checkAll = True
        elif opt in ("--file", "-f"):
            path = arg
    
    if(length == 0):
        print("Error: No length given")
        print('Usage: dictionary.py -l <int> (-p <string>) (-s <string>) (--checkAll)')
        sys.exit()
    
    if(getInputLength() < length):
        openFile(path)
        openDict()
        StartLoop()
    else:
        print("length is lower than prefix + suffix")

if __name__ == "__main__":
    start(sys.argv[1:])