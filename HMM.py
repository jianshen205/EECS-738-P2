"""
file@ HMM.py
author@ Brian Quiroz, Jian Shen
date@ Mar 18, 2019
"""
import numpy as np
import random
import string

firstWords = {}
secondWords = {}
thirdWords = {}
transitions = {}

def tokenize(row):
    #cutting into words and removing punctuation
    tokens = row.rstrip().lower()
    tokens = tokens.translate(str.maketrans('','', string.punctuation)).split()
    return tokens

def updateValueInDict(dict, key):
    dict[key] = firstWords.get(key, 0) + 1

def insertValue(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)

def normalize(dict, sum):
    for key in dict.keys():
        dict[key] /= sum

def listToDict(dict, word):
    list = dict[word]
    subDict = {}
    listLength = len(list)
    for num in list:
        updateValueInDict(subDict, num)
    normalize(subDict, listLength)

def getRandomValueFromDict(dict):
    return random.choice(list(set(dict)))

def readFromFile():
    ##read lines from file
    file = open("shakespeare-plays/alllines.txt")
    rows = file.read().splitlines() #split the lines at line boundaries returns a list of lines
    # lines = []
    return rows


def train(rows):
    for i in range(0,len(rows)):
        original = rows[i]
        # rows[i] = original.replace("\"","") ##delete quotation mark from each line
        # print (rows[:5]) ##test retrieved data if correct
        tokens = tokenize(original)
        amountOfTokens = len(tokens)

        for i in range(0, amountOfTokens):
            token = tokens[i]
            if i == 0:
                updateValueInDict(firstWords, token)

            else:
                if i == 1:
                    insertValue(secondWords, tokens[i - 1], token)
                elif i == 2:
                    insertValue(thirdWords, (tokens[i - 2], tokens[i - 1]), token)
                else:
                    insertValue(transitions, (tokens[i - 3], tokens[i - 2], tokens[i - 1]), token)

                if i == amountOfTokens - 1 and amountOfTokens > 1:
                    insertValue(transitions, (tokens[i - 2], tokens[i - 1], token), 'tokEND')

    firstWordsSum = sum(firstWords.values())
    normalize(firstWords, firstWordsSum)

    for word in secondWords.keys():
        listToDict(secondWords, word)

    for word in thirdWords.keys():
        listToDict(thirdWords, word)

    for word in transitions.keys():
        listToDict(transitions, word)


def generateLine():
    line = []
    first = getRandomValueFromDict(firstWords)
    line.append(first)
    if first in secondWords.keys():
        second = getRandomValueFromDict(secondWords[first])
        line.append(second)
        if (first, second) in thirdWords.keys():
            third = getRandomValueFromDict(thirdWords[(first, second)])
            line.append(third)
        else:
            third = "tokEND"
    else:
        second = "tokEND"

    if (not third == "tokEND" and not second == "tokEND"):
        next = ""
        while(not next == "tokEND"):
            if (first, second, third) in transitions.keys():
                next = getRandomValueFromDict(transitions[(first, second, third)])
                if (not next == "tokEND"):
                    line.append(next)
                    first = second
                    second = third
                    third = next
            else:
                next = "tokEND"

    return line

def main():
    data = readFromFile()
    print("Training...")
    train(data)
    numberOfPlays = 30
    for i in range(0, numberOfPlays):
        line = generateLine()
        print(' '.join(line))

if __name__== "__main__":
  main()
