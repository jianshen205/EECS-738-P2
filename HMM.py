"""
file@ HMM.py
author@ Brian Quiroz, Jian Shen
date@ Mar 18, 2019
"""
import numpy as np
import random
import string

firstWords = {}
pairs = {}
triples = {}
transitions = {}

NUMBER_OF_LINES = 30
MAX_NUMBER_OF_WORDS_PER_LINE = 20
end = "tokEND"

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
    return subDict

def getRandomValueFromDict(dict, key):
    if dict == firstWords:
        return random.choice(list(set(dict)))
    else:
        if key in dict:
            subDict = dict[key]
            if len(subDict) > 1:
                return random.choice(list(set(subDict)))
            else:
                if dict == transitions:
                    attempt1 = getRandomValueFromDict(triples, (key[1],key[2]))
                    if attempt1 == end:
                        attempt2 = getRandomValueFromDict(pairs, key[1])
                        if attempt2 == end:
                            return random.choice(list(set(subDict)))
                        else:
                            return attempt2
                    else:
                        return attempt1

                elif dict == triples:
                    attempt = getRandomValueFromDict(pairs, key[1])
                    if attempt == end:
                        return random.choice(list(set(subDict)))
                    else:
                        return attempt

                else:
                    return random.choice(list(set(subDict)))
        else:
            # print(key,"NOT FOUND")
            return end

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
                    insertValue(pairs, tokens[i - 1], token)
                elif i == 2:
                    insertValue(triples, (tokens[i - 2], tokens[i - 1]), token)
                else:
                    insertValue(transitions, (tokens[i - 3], tokens[i - 2], tokens[i - 1]), token)

                if i == amountOfTokens - 1 and amountOfTokens > 1:
                    insertValue(transitions, (tokens[i - 2], tokens[i - 1], token), end)

    firstWordsSum = sum(firstWords.values())
    normalize(firstWords, firstWordsSum)

    for word in pairs.keys():
        pairs[word] = listToDict(pairs, word)

    for word in triples.keys():
        triples[word] = listToDict(triples, word)

    for word in transitions.keys():
        transitions[word] = listToDict(transitions, word)

    # print(firstWords)
    # print(pairs)
    # print(triples)
    # print(transitions)


def generateLine():
    line = []
    first = getRandomValueFromDict(firstWords,"")
    line.append(first)

    second = getRandomValueFromDict(pairs, first)
    third = end
    if not second == end:
        line.append(second)
        third = getRandomValueFromDict(triples, (first, second))
        if not third == end:
            line.append(third)
        else:
            third = getRandomValueFromDict(pairs, second)
            if not third == end:
                # print("Third worked with pairs!")
                line.append(third)
            else:
                third = end
    else:
        second = end

    if (not third == end and not second == end):
        next = ""
        while(not next == end and len(line) <= MAX_NUMBER_OF_WORDS_PER_LINE):
            next = getRandomValueFromDict(transitions,(first, second, third))
            if not next == end:
                line.append(next)
                first = second
                second = third
                third = next
            else:
                next = getRandomValueFromDict(triples, (second, third))
                if not next == end:
                    # print("Next worked with triples!")
                    line.append(next)
                    first = second
                    second = third
                    third = next
                else:
                    next = getRandomValueFromDict(pairs, third)
                    if not next == end:
                        # print("Next worked with pairs!")
                        line.append(next)
                        first = second
                        second = third
                        third = next
                    else:
                        next = end

    return line

def main():
    data = readFromFile()
    print("Training...")
    train(data)
    play = []
    for i in range(0, NUMBER_OF_LINES):
        line = generateLine()
        play.append(' '.join(line))

    print("Play:",'\n')
    for line in play:
        print(line,'\n')

if __name__== "__main__":
  main()
