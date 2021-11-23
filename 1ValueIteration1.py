import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from Animate import generateAnimat


def main(argv):
    gamma = 0.9
    endChange = 0.005

    width = int(sys.argv[1])
    height = int(sys.argv[2])
    numArguments = len(sys.argv) - 1
    numBomb = 3

    startX = random.randint(0, width - 1)
    startY = random.randint(0, height - 1)

    endX = random.randint(0, width - 1)
    endY = random.randint(0, height - 1)

    while ((endX, endY) == (startX, startY)):
        endX = random.randint(0, width - 1)
        endY = random.randint(0, height - 1)

    record = []

    # print(width)
    # print(height)

    if (numArguments > 2):
        for i in range(3, numArguments):

            if (sys.argv[i] == "-start"):
                startX = int(sys.argv[i + 1])
                startY = int(sys.argv[i + 2])

            if (sys.argv[i] == "-end"):
                endX = int(sys.argv[i + 1])
                endY = int(sys.argv[i + 2])

            if (sys.argv[i] == "-k"):
                numBomb = int(sys.argv[i + 1])

            if (sys.argv[i] == "-gamma"):
                gamma = float(sys.argv[i + 1])

            # initialize landmines coordinates
    landMines = []
    for i in range(0, numBomb):
        tempX = random.randint(0, width - 1)
        tempY = random.randint(0, height - 1)
        if (not (tempX, tempY) in landMines) and ((tempX, tempY) != (startX, startY)) and (
                (tempX, tempY) != (endX, endY)):
            landMines.append((tempX, tempY))
        else:
            while (((tempX, tempY) in landMines) or ((tempX, tempY) == (startX, startY)) or (
                    (tempX, tempY) == (endX, endY))):
                tempX = random.randint(0, width - 1)
                tempY = random.randint(0, height - 1)
            landMines.append((tempX, tempY))

    # initialize state list
    states = []
    for j in range(0, height):
        for i in range(0, width):
            states.append((i, j))

    # print("states: ")
    # print( states ) ;

    # initialize rewards list
    rewards = {}
    for i in states:
        if i == (startX, startY):
            rewards[i] = 0
        elif i == (endX, endY):
            rewards[i] = 1
        elif i in landMines:
            rewards[i] = -1
        else:
            rewards[i] = 0

    # initialize action dictionary
    actions = {
        (0, 0): ('D', 'R'),
        (width - 1, height - 1): ('U', 'L'),
        (width - 1, 0): ('D', 'L'),
        (0, height - 1): ('U', 'R'),
    }
    for i in range(0, width):
        for j in range(0, height):
            if (((i, j) != (0, 0)) and ((i, j) != (width - 1, height - 1)) and ((i, j) != (width - 1, 0)) and (
                    (i, j) != (0, height - 1)) and ((i, j) not in landMines) and ((i, j) != (endX, endY))):
                if (j == 0):
                    actions.update({(i, j): ('D', 'L', 'R')})
                elif (i == 0):
                    actions.update({(i, j): ('D', 'U', 'R')})
                elif (i == width - 1):
                    actions.update({(i, j): ('D', 'U', 'L')})
                elif (j == height - 1):
                    actions.update({(i, j): ('U', 'L', 'R')})
                else:
                    actions.update({(i, j): ('D', 'U', 'L', 'R')})

    # print("actions: ")
    # print( actions ) ;

    # initialize policy dictionary
    policy = {}
    for s in actions.keys():
        n = random.randint(0, len(actions[s]) - 1)
        # print(len( actions[s] ))

        tempCoord = actions.get(s);
        templist = []
        for direction in tempCoord:
            templist.append(direction)

        policy[s] = templist[n]

    # print("policy: ")
    # print( policy ) ;

    # initialize value dictionary
    value = {}
    for s in states:
        if s in actions.keys():
            value[s] = 0
        if s == (startX, startY):
            value[s] = 0
        if s == (endX, endY):
            value[s] = 100
        if s in landMines:
            value[s] = -1

    # print("value: ")
    # print( value ) ;

    record.append([])
    for j in range(0, height):
        tempAdd = []
        for i in range(0, width):
            tempAdd.append(value[i, j])
        record[0].append(tempAdd)

    # iteration to find the optimal policy
    iteration = 1
    while True:
        changeValue = 0

        tempValue = value.copy()

        for i in states:

            # if i in landMines:
            #  continue
            # if i == (endX,endY):
            #  continue

            if i in policy:
                # i is the coordinate such as (0,0)

                currentValue = value[i]
                nextValue = 0

                # print("new state")

                for j in actions[i]:
                    if j == 'U':
                        newCoord = (i[0], i[1] - 1)
                    if j == 'D':
                        newCoord = (i[0], i[1] + 1)
                    if j == 'L':
                        newCoord = (i[0] - 1, i[1])
                    if j == 'R':
                        newCoord = (i[0] + 1, i[1])

                    # tempCalcValue = rewards[i] + gamma * value[newCoord]
                    tempCalcValue = rewards[i] + gamma * tempValue[newCoord]
                    if tempCalcValue > nextValue:
                        nextValue = tempCalcValue
                        policy[i] = j

                value[i] = nextValue
                changeValue = max(changeValue, abs(currentValue - nextValue))

        if changeValue < endChange:
            break

        record.append([])
        for j in range(0, height):
            tempAdd = []
            for i in range(0, width):
                tempAdd.append(value[i, j])
            record[iteration].append(tempAdd)
        iteration += 1

        # print("record")
        # print(record)

    print("itertaion: " + str(iteration))

    # print("final policy:")
    # print(policy)

    opt_pol = [(startX, startY)]

    finalRouteCoord = (startX, startY)
    while (finalRouteCoord != (endX, endY)):
        if policy[finalRouteCoord] == 'U':
            finalRouteCoord = (finalRouteCoord[0], finalRouteCoord[1] - 1)
        elif policy[finalRouteCoord] == 'D':
            finalRouteCoord = (finalRouteCoord[0], finalRouteCoord[1] + 1)
        elif policy[finalRouteCoord] == 'L':
            finalRouteCoord = (finalRouteCoord[0] - 1, finalRouteCoord[1])
        elif policy[finalRouteCoord] == 'R':
            finalRouteCoord = (finalRouteCoord[0] + 1, finalRouteCoord[1])

        opt_pol.append(finalRouteCoord)

    print("opt_pol:")
    print(opt_pol)

    anim, fig, ax = generateAnimat(record, (startX, startY), (endX, endY), mines=landMines, opt_pol=opt_pol,
                                   start_val=-10, end_val=100, mine_val=150, just_vals=False, generate_gif=False,
                                   vmin=-10, vmax=150)

    plt.show()


if __name__ == '__main__':
    main(sys.argv[1:])