import sys, getopt
import zlib

dictionary = []
prefix = ''
suffix = ''
length = 0
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
        hashes.append(x.lower().strip())

def doCRC(string):
    return hex(zlib.crc32(bytearray(string, 'utf-8')))

def check(string):
    global prefix, suffix
    hash = doCRC(prefix + string + suffix)
    if hash in hashes:
        print("{0} -> {1} length: {2}".format(hash, prefix + string + suffix, len(prefix + string + suffix)))

def process(prevWords, prevWord, string):
    global length, checkAll
    if(checkAll):
        if(len(string) + getInputLength() < length):
            check(string)
            loop(prevWords, prevWord, string)
    else:
        if(len(string) + getInputLength() == length):
            check(string)
        else:
            if(len(string)  + getInputLength() < length):
                loop(prevWords, prevWord, string)

def loop(prevWords, prevWord, string):
    global dictionary
    for word in dictionary:
        if(word not in prevWords):
            if(prevWord != "_" and word != "_"):
                words = prevWords.copy()
                if(word != "_"):
                    words.append(word)
                process(words, word, string + "_" + word)

#Prints first character to show progress
def StartLoop():
    global dictionary
    for word in dictionary:
        print(word)
        process([word], word, word)

def start(argv):
    global defaultPath, prefix, suffix, length, checkAll
    path = defaultPath
    try:
      opts, args = getopt.getopt(argv,"hl:p:s:f",["suffix=","prefix=","length=", "checkAll", "file="])
    except getopt.GetoptError:
        print('dictionary.py -l <int> (-p <string>) (-s <string>) (--checkAll)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('dictionary.py -l <int> (-p <string>) (-s <string>) (--checkAll)')
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