"""
file@ HMM.py
author@ Brian Q, Jian Shen
date@ Mar 18, 2019
"""
import numpy as np

##read lines from file
file = open("shakespeare-plays/alllines.txt")
rows = file.read().splitlines() #split the lines at line boundaries returns a list of lines
lines = []
for i in range(0,len(rows)):
    original = rows[i]
    rows[i] = original.replace("\"","") ##delete quotation mark from each line
#print rows[:5] ##test retrieved data if correct

