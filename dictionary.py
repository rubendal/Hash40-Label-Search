import sys, getopt
import zlib
from hash40 import Hash40

dictionary = []
prefix = ''
suffix = ''
depth = 2
hashes = []
repeat = True
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

def checkLoop(currentDepth, prevWords, prevWord, string):
    global depth
    if(depth == 0):
        loop(currentDepth, prevWords, prevWord, string)
    else:
        if(currentDepth < depth):
            loop(currentDepth, prevWords, prevWord, string)

def process(currentDepth, prevWords, prevWord, string):
    check(string)
    checkLoop(currentDepth + 1, prevWords, prevWord, string)

def loop(currentDepth, prevWords, prevWord, string):
    global dictionary, repeat
    for word in dictionary:
        if not repeat:
            if(word not in prevWords):
                if(prevWord != "_" and word != "_"):
                    words = prevWords.copy()
                    if(word != "_"):
                        words.append(word)
                    process(currentDepth, words, word, string + "_" + word)
        else:
            process(currentDepth, [], word, string + "_" + word)

#Prints first character to show progress
def StartLoop():
    global dictionary
    for word in dictionary:
        print(word)
        process(0, [word], word, word)

#Prints first character to show progress
def StartLoopFromWord(first):
    global dictionary
    used = False
    for word in dictionary:
        if used:
            print(word)
            process(0, [word], word, word)
        else:
            if word == first:
                used = True
                print(word)
                process(0, [word], word, word)

def start(argv):
    global defaultPath, prefix, suffix, depth, repeat
    path = defaultPath
    first = None
    try:
      opts, args = getopt.getopt(argv,"h:d:p:s:f",["suffix=","prefix=", "file=", "depth=", "startFrom=", "noRepeat"])
    except getopt.GetoptError:
        print('dictionary.py (-d <int>) (-p <string>) (-s <string>) (--startFrom=<string>) (--noRepeat)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dictionary.py -l <int> (-p <string>) (-s <string>) (--startFrom=<string>) (--noRepeat)')
            print("-d/--depth= <int>: Max amount of words to use (prefix/suffix not counted)")
            print("-p/--prefix= <string>: Prefix to add to generated strings")
            print("-s/--suffix= <string>: Suffix to add to generated strings")
            print("--startFrom= <string> Word to start checking from dictionary")
            print("--noRepeat Prevents string from having words that have been used (not counting prefix and suffix)")
            sys.exit()
        elif opt in ("--prefix", "-p"):
            prefix = arg
        elif opt in ("--sufix", "-s"):
            suffix = arg
        elif opt in ("--depth", "-d"):
            depth = int(arg)
        elif opt in ("--file", "-f"):
            path = arg
        elif opt in ("--startFrom"):
            first = arg
        elif opt in ("--noRepeat"):
            repeat = False
    
    if depth > 0:
        openFile(path)
        openDict()
        if first is None:
            StartLoop()
        else:
            StartLoopFromWord(first)
    else:
        print("error: depth cannot be lower than 1")

if __name__ == "__main__":
    start(sys.argv[1:])