# CSC3022F - RL Assignment 2
# Part 1
# packages
import matplotlib.pyplot as plt
import sys
import random
import numpy



#import from animate.py
from Animate import generateAnimat

#
width = 0
height = 0
startpos = [0,0]
endpos = [0,0]
gamma = 0.8
k = 3
mines = []
records = []
opt = []


def checkmine(test,array):
    return any(numpy.array_equal(x, test) for x in array)

def check_conv():
    if len(records) > 1:
        comparison = records[len(records)-2] == records[len(records)-1]
        equal = comparison.all()
        return equal
    return False


def V_Iteration():
    count = 0
    maxarray = [0,0,0,0,0]
    while count == 0:
        temparray = records[len(records)-1].copy()
        for i in range(0,height):
            for j in range(0,width):
                if checkmine([j,i],mines) == False:
                    maxarray = [0, 0, 0, 0 ,temparray[i][j]]
                    #up
                    if i != 0:
                        maxarray[0] = gamma*temparray[i-1][j]
                    #down
                    if i != height-1:
                        maxarray[1] = gamma*temparray[i+1][j]
                    #left
                    if j != 0:
                        maxarray[2] = gamma*temparray[i][j-1]
                    #right
                    if j != width-1:
                        maxarray[3] = gamma*temparray[i][j+1]
                    temparray[i][j] = max(maxarray)
                else:
                    temparray[i][j] = 0


        records.append(temparray)
        if check_conv() == True:
            break


def optimal():
    global opt
    temparray = records[len(records) - 1]
    maxarray = [0, 0, 0, 0]
    count = 0
    x = startpos[1]
    y = startpos[0]
    # append the start position first
    opt.append(startpos)
    while count == 0:

        if x == endpos[1] and y == endpos[0]:
            break;
        # up
        if x != 0:
            maxarray[0] = temparray[x - 1][y]
        # down
        if x != height - 1:
            maxarray[1] = temparray[x + 1][y]
        # left
        if y != 0:
            maxarray[2] = temparray[x][y - 1]
        # right
        if y != width - 1:
            maxarray[3] = temparray[x][y + 1]
        max_value = max(maxarray)
        max_index = numpy.where(maxarray == max_value)
        if max_index[0][0] == 0:
            x -= 1
        elif max_index[0][0] == 1:
            x += 1
        elif max_index[0][0] == 2:
            y -= 1
        elif max_index[0][0] == 3:
            y += 1
        opt.append([y, x])

def main(argv):

    global width ,height, startpos, endpos, gamma, k, records, mines
    count = 0
    width = int(argv[0])
    height = int(argv[1])
    endpos = [width - 1, height - 1]
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

    #first record(iteration 0)
    temptwo = numpy.zeros((height,width),dtype=int)
    temptwo[endpos[1]][endpos[0]] = 100
    records.append(temptwo)


if __name__ == '__main__':
    main(sys.argv[1:])
    V_Iteration()
    optimal()

    anim, fig, ax = generateAnimat(records, startpos, endpos, mines=mines, opt_pol=opt,
                                   start_val=-10, end_val=100, mine_val=150, just_vals=False, generate_gif=False,
                                   vmin=-10, vmax=150)

    plt.show()