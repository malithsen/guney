#!/usr/bin/python

import re
import random
import sys
import codecs

tempMapping = {}

mapping = {}

starts = []

def toHashKey(lst):
    return tuple(lst)

def wordlist(filename):
    f = codecs.open(filename,"r","utf-16")
    wordlist = [w for w in re.findall(r"[^\x00-\x7F']+|[.,!?;]", f.read())]
    f.close()
    return wordlist

def addItemToTempMapping(history, word):
    global tempMapping
    while len(history) > 0:
        first = toHashKey(history)
        if first in tempMapping:
            if word in tempMapping[first]:
                tempMapping[first][word] += 1.0
            else:
                tempMapping[first][word] = 1.0
        else:
            tempMapping[first] = {}
            tempMapping[first][word] = 1.0
        history = history[1:]

# Building and normalizing the mapping.
def buildMapping(wordlist, markovLength):
    global tempMapping
    starts.append(wordlist [0])
    for i in range(1, len(wordlist) - 1):
        if i <= markovLength:
            history = wordlist[: i + 1]
        else:
            history = wordlist[i - markovLength + 1 : i + 1]
        follow = wordlist[i + 1]
        # if the last elt was a period, add the next word to the start list
        if history[-1] == "." and follow not in ".,!?;":
            starts.append(follow)
        addItemToTempMapping(history, follow)
    # Normalize the values in tempMapping, put them into mapping
    for first, followset in tempMapping.iteritems():
        total = sum(followset.values())
        mapping[first] = dict([(k, v / total) for k, v in followset.iteritems()])

def next(prevList):
    sum = 0.0
    retval = ""
    index = random.random()
    # Shorten prevList until it's in mapping
    while toHashKey(prevList) not in mapping:
        prevList.pop(0)
    # Get a random word from the mapping, given prevList
    for k, v in mapping[toHashKey(prevList)].iteritems():
        sum += v
        if sum >= index and retval == "":
            retval = k
    return retval

def genSentence(markovLength, seed = None):
    # Start with a random "starting word"
    if not seed:
        curr = random.choice(starts)
    else:
        curr = seed.split()
        curr = curr[0].decode('utf-8')

    sent = curr.capitalize()
    prevList = [curr]
    # Keep adding words until we hit a period
    while (curr not in "."):
        # print 'prevList', prevList
        curr = next(prevList)
        prevList.append(curr)
        # if the prevList has gotten too long, trim it
        if len(prevList) > markovLength:
            prevList.pop(0)
        if (curr not in ".,!?;"):
            sent += " " # Add spaces between words (but not punctuation)
        sent += curr
    return sent

def main():
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: ' + sys.argv [0] + ' text_source [chain_length=1] [sinhala=None]\n')
        sys.exit(1)

    filename = sys.argv[1]
    markovLength = 1
    if len (sys.argv) == 3:
        markovLength = int(sys.argv [2])

    buildMapping(wordlist(filename), markovLength)

    while True:
        seed = raw_input('> ')
        res = genSentence(markovLength, seed)
        print (res)
        print '\n'
        f.write(seed.decode('utf-8'))
        f.write('> ' + res)
        f.write('\n')
        
        

if __name__ == "__main__":
    try:
        f = codecs.open("res.txt", "w", "utf-16")
        main()
    except KeyboardInterrupt:
        print ("Bye bye")
        f.close() 