# CSC3022F - RL Assignment 2
# Part 1
# packages
import matplotlib.pyplot as plt
import sys
import random



#import from animate.py
from Animate import generateAnimat

#
width = 0
height = 0
startpos = [0,0]
endpos = [0,0]
gamma = 0.8
k = 0
mines = []
records = []

def main(argv):

    global width ,height, startpos, endpos, gamma, k, records, mines
    count = 0
    width = int(argv[0])
    height = int(argv[1])
    endpos = [height - 1, height - 1]
    while count < len(argv):
       if argv[count] == "-start":
           startpos = [int(argv[count + 1]), int(argv[count + 2])]
           count += 1
       elif argv[count] == "-end":
           endpos = [int(argv[count + 1]), int(argv[count + 2])]
           count += 1
       elif argv[count] == "-gamma":
           gamma = float(argv[count + 1])
       elif argv[count] == "-k":
           k = int(argv[count + 1])
       count += 1


if __name__ == '__main__':
    main(sys.argv[1:])

