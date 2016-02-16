#!/usr/bin/python

import re
import random
import sys
import codecs

class Markov:
    def __init__(self):
        self.tempMapping = {}
        self.mapping = {}
        self.starts = []
        filename = 'all.txt'
        self.markovLength = 1
        self.buildMapping(self.wordlist(filename), self.markovLength)

    def toHashKey(self, lst):
        return tuple(lst)

    def wordlist(self, filename):
        f = codecs.open(filename,"r","utf-16")
        wordlist = [w for w in re.findall(r"[^\x00-\x7F']+|[.,!?;]", f.read())]
        f.close()
        return wordlist

    def addItemToTempMapping(self, history, word):
        while len(history) > 0:
            first = self.toHashKey(history)
            if first in self.tempMapping:
                if word in self.tempMapping[first]:
                    self.tempMapping[first][word] += 1.0
                else:
                    self.tempMapping[first][word] = 1.0
            else:
                self.tempMapping[first] = {}
                self.tempMapping[first][word] = 1.0
            history = history[1:]

    # Building and normalizing the mapping.
    def buildMapping(self, wordlist, markovLength):
        self.starts.append(wordlist [0])
        for i in range(1, len(wordlist) - 1):
            if i <= markovLength:
                history = wordlist[: i + 1]
            else:
                history = wordlist[i - markovLength + 1 : i + 1]
            follow = wordlist[i + 1]
            # if the last elt was a period, add the next word to the start list
            if history[-1] == "." and follow not in ".,!?;":
                self.starts.append(follow)
            self.addItemToTempMapping(history, follow)
        # Normalize the values in tempMapping, put them into mapping
        for first, followset in self.tempMapping.iteritems():
            total = sum(followset.values())
            self.mapping[first] = dict([(k, v / total) for k, v in followset.iteritems()])

    def next(self, prevList):
        sum = 0.0
        retval = ""
        index = random.random()
        # Shorten prevList until it's in mapping
        while self.toHashKey(prevList) not in self.mapping:
            prevList.pop(0)
        # Get a random word from the mapping, given prevList
        for k, v in self.mapping[self.toHashKey(prevList)].iteritems():
            sum += v
            if sum >= index and retval == "":
                retval = k
        return retval

    def genSentence(self, markovLength, seed = None):
        # Start with a random "starting word"
        if not seed:
            curr = random.choice(self.starts)
        else:
            curr = seed.split()
            curr = curr[0]

        sent = curr.capitalize()
        prevList = [curr]
        # Keep adding words until we hit a period
        while (curr not in "."):
            # print 'prevList', prevList
            curr = self.next(prevList)
            prevList.append(curr)
            # if the prevList has gotten too long, trim it
            if len(prevList) > markovLength:
                prevList.pop(0)
            if (curr not in ".,!?;"):
                sent += " " # Add spaces between words (but not punctuation)
            sent += curr
        return sent

    def main(self, seed):
        res = self.genSentence(self.markovLength, seed)
        return res
