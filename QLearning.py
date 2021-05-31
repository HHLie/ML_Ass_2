# CSC3022F - RL Assignment 2
# Part 2
# packages
import matplotlib.pyplot as plt
import sys
import random
import numpy
import math

# import from animate.py
from Animate import generateAnimat

#
width = 0
height = 0
startpos = [0, 0]
endpos = [0, 0]
gamma = 0.8
k = 3
mines = []
records = []
opt = []
epoch = 50
learning_rate = 0.5

# used to check if given coord test is within the given array, i used this mostly to check if the coord is a mine
def checkmine(test, array):
    return any(numpy.array_equal(x, test) for x in array)



# get the optimal position by looking for the max value of the neighbouring states
def optimal():
    global opt
    temparray = records[len(records) - 1]
    count = 0
    x = startpos[1]
    y = startpos[0]
    # append the start position first
    opt.append(startpos)
    while count == 0:
        oldx = x
        oldy = y
        maxarray = [0, 0, 0, 0]
        if x == endpos[1] and y == endpos[0]:
            break;
        # up
        if x > 0:
            maxarray[0] = temparray[x - 1][y]
        # down
        if x < height - 1:
            maxarray[1] = temparray[x + 1][y]
        # left
        if y > 0:
            maxarray[2] = temparray[x][y - 1]
        # right
        if y < width - 1:
            maxarray[3] = temparray[x][y + 1]
        max_value = max(maxarray)
        max_index = numpy.where(maxarray == max_value)
        max_i = numpy.argmax(maxarray)
        if len(max_index[0]) - 1 < 0:
            return False
        if max_i == 0:
            x -= 1
        elif max_i == 1:
            x += 1
        elif max_i == 2:
            y -= 1
        elif max_i == 3:
            y += 1
        opt.append([y, x])
        temparray[oldx][oldy] = -1
    return True


def main(argv):
    global width, height, startpos, endpos, gamma, k, records, mines, epoch, learning_rate
    # parameter handling
    count = 0
    width = int(argv[0])
    height = int(argv[1])
    endpos = [width - 1, height - 1]
    startpos = [0, 0]
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
        elif argv[count] == "-epoch":
            epoch = int(argv[count + 1])
        elif argv[count] == "-learning":
            learning_rate = float(argv[count + 1])
        count += 1

    temptwo = numpy.zeros((height, width), dtype=int)

    # set mines

    if k > 0:
        r_height = [*range(0, height)]
        r_width = [*range(0, width)]
        count = 0
        while len(mines) < k:
            temp_x = random.choice(r_width)
            temp_y = random.choice(r_height)
            if [temp_x, temp_y] == endpos:
                count += 0
            elif [temp_x, temp_y] == startpos:
                count += 0
            elif checkmine([temp_x, temp_y], mines):
                count += 0
            else:
                mines.append([temp_x, temp_y])

    # first record(iteration 0)
    temptwo[endpos[1]][endpos[0]] = 100
    records.append(temptwo)
