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

    #set mines
    if k > 0:
        r_height = [*range(0, height)]
        r_width = [*range(0, width)]

        if startpos[0] in r_width:
            r_width.remove(startpos[0])
        if endpos[1] in r_height:
            r_height.remove(endpos[1])
        for i in range(0,k):
            temp_x = random.choice(r_width)
            temp_y = random.choice(r_height)
            mines.append([temp_x,temp_y])



if __name__ == '__main__':
    main(sys.argv[1:])

