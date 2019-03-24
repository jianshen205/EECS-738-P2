"""
file@ HMM.py
author@ Brian Q, Jian Shen
date@ Mar 18, 2019
"""
import numpy as np
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

def insertValue(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)

def readFromFile():
    ##read lines from file
    file = open("shakespeare-plays/alllines.txt")
    rows = file.read().splitlines() #split the lines at line boundaries returns a list of lines
    lines = []
    return rows

def train(rows):
    for i in range(0,len(rows)):#(0,len(rows))
        original = rows[i]
        # rows[i] = original.replace("\"","") ##delete quotation mark from each line
    #print rows[:5] ##test retrieved data if correct


        tokens = tokenize(rows[i])
        amountOfTokens = len(tokens)

        for i in range(0, amountOfTokens):
            token = tokens[i]
            if i == 0:
                firstWords[token] = firstWords.get(token, 0) + 1

            else:
                if i == 1:
                    insertValue(secondWords, tokens[i - 1], token)
                elif i == 2:
                    insertValue(thirdWords, (tokens[i - 2], tokens[i - 1]), token)
                else:
                    insertValue(transitions, (tokens[i - 3], tokens[i - 2], tokens[i - 1]), token)

                if i == amountOfTokens - 1 and amountOfTokens > 1:
                    insertValue(transitions, (tokens[i - 2], tokens[i - 1], token), 'tokEND')

#PRINT FOR DEBUGGING
    # print(firstWords)
    # print("\n\n\n")
    # print(secondWords)
    # print("\n\n\n")
    # print(thirdWords)
    # print("\n\n\n")
    # print(transitions)
    # print("\n\n\n")

def main():
    data = readFromFile()
    train(data)

if __name__== "__main__":
  main()
