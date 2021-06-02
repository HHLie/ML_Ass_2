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

# global variables
width = 0
height = 0
startpos = [0, 0]
endpos = [0, 0]
gamma = 0.8
k = 3
mines = []
records = []
opt = []
epoch = 500
learning_rate = 0.3

# used to check if given coord test is within the given array, i used this mostly to check if the coord is a mine
def checkmine(test, array):
    return any(numpy.array_equal(x, test) for x in array)

#do Qlearning algorithm
def Q_learn():
    global gamma, records, endpos, learning_rate
    R = records[len(records) - 1].copy()
    for i in range(len(mines)):
        R[mines[i][1]][mines[i][0]] = -50
    Q = R.copy()
    #Q = numpy.zeros((height, width), dtype=int)
    randpos = []
    e = 10
    #epoch loop
    for i in range(epoch):
        if learning_rate <= 0.01:
            break
        r_height = [*range(0, height)]
        r_width = [*range(0, width)]
        count = 0
        # generate random position till not mine or end state
        while True:
            randpos.clear()
            temp_x = random.choice(r_width)
            temp_y = random.choice(r_height)
            if checkmine([temp_x, temp_y], mines):
                count += 0
            else:
                randpos = [temp_x, temp_y]
                break
        #choose random position move till terminal state
        while randpos != endpos or not checkmine(randpos,mines):

            count += 1
            # choose action
            action = ["up", "down", "left", "right"]
            max_ar = []
            next_action = randpos.copy()
            # check if position is on the edge if so remove action that leads to out of bounds
            if randpos[1] == 0:
                action.remove("up")
            if randpos[1] == height - 1:
                action.remove("down")
            if randpos[0] == 0:
                action.remove("left")
            if randpos[0] == width - 1:
                action.remove("right")
            # get next random action
            choice = random.choice(action)
            if choice == "up":
                next_action = [randpos[0],randpos[1]-1]
            if choice == "down":
                next_action = [randpos[0],randpos[1]+1]
            if choice == "left":
                next_action = [randpos[0]-1,randpos[1]]
            if choice == "right":
                next_action = [randpos[0] +1, randpos[1]]

            # get max of next states
            temp_pos = randpos.copy()
            temp_max = 0
            for i in range(len(action)):
                if "up" == action[i]:
                    max_ar.append(Q[randpos[1] - 1][randpos[0]])
                    if Q[randpos[1] - 1][randpos[0]] >= temp_max:
                        temp_max = Q[randpos[1] - 1][randpos[0]].copy()
                        temp_pos = [randpos[0],randpos[1] - 1]
                if "down" == action[i]:
                    max_ar.append(Q[randpos[1] + 1][randpos[0]])
                    if Q[randpos[1] + 1][randpos[0]] >= temp_max:
                        temp_max = Q[randpos[1] + 1][randpos[0]].copy()
                        temp_pos = [randpos[0],randpos[1] + 1]
                if "left" == action[i]:
                    max_ar.append(Q[randpos[1]][randpos[0] - 1])
                    if Q[randpos[1]][randpos[0]-1] >= temp_max:
                        temp_max = Q[randpos[1]][randpos[0]-1].copy()
                        temp_pos = [randpos[0]-1,randpos[1]]
                if "right" == action[i]:
                    max_ar.append(Q[randpos[1]][randpos[0] + 1])
                    if Q[randpos[1]][randpos[0]+1] >= temp_max:
                        temp_max = Q[randpos[1]][randpos[0]-1].copy()
                        temp_pos = [randpos[0]+1,randpos[1]]
            currentQ = Q[randpos[1]][randpos[0]]
            factor = random.randint(1, 10)
            # if random number 1-10 is less than e greedy value, choose random action
            # 1-10 is the same as using e{0,1}
            if factor < int(e):
                #compute reward value for random action
                Q[randpos[1]][randpos[0]] = math.floor(currentQ + learning_rate*(R[randpos[1]][randpos[0]] + (gamma * Q[next_action[1]][next_action[0]] - currentQ)))
                randpos = next_action
            else:
                # compute reward value for best action
                Q[randpos[1]][randpos[0]] = math.ceil(currentQ + learning_rate*(R[randpos[1]][randpos[0]] + (gamma * max(max_ar) - currentQ)))
                randpos = temp_pos

            if(randpos == temp_pos):
                break

            max_ar.clear()

        records.append(Q.copy())
        #decay the learning rate
        learning_rate = learning_rate - learning_rate*(1 / (epoch + i + count))
        if e > 1:
            e = e - e*(i/(epoch/2))


# get the optimal position by looking for the max value of the neighbouring states
def optimal():
    global opt
    temparray = records[len(records) - 1].copy()
    for i in range(len(mines)):
        temparray[mines[i][1]][mines[i][0]] = -5000
    count = 0
    x = startpos[1]
    y = startpos[0]
    # append the start position first
    opt.append(startpos)
    while count == 0:
        oldx = x
        oldy = y
        maxarray = [-100, -100, -100, -100]
        if x == endpos[1] and y == endpos[0]:
            break;
        # up
        if x > 0 and not checkmine((y,x - 1), mines):
            maxarray[0] = temparray[x - 1][y]
        # down
        if x < height - 1 and not checkmine((y,x + 1),mines):
            maxarray[1] = temparray[x + 1][y]
        # left
        if y > 0 and not checkmine((y-1,x),mines):
            maxarray[2] = temparray[x][y - 1]
        # right
        if y < width - 1 and not checkmine((y+1,x),mines):
            maxarray[3] = temparray[x][y + 1]
        max_value = max(maxarray)
        #print(maxarray)
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
        temparray[oldx][oldy] = -100
    return True


def main(argv):
    global width, height, startpos, endpos, gamma, k, records, mines, epoch, learning_rate
    # parameter handling
    count = 0
    width = int(argv[0])
    height = int(argv[1])
    endpos = [width - 1, height - 1]
    startpos = [0, 0]

    r_height = [*range(0, height)]
    r_width = [*range(0, width)]
    temp_x = random.choice(r_width)
    temp_y = random.choice(r_height)
    startpos = [temp_x,temp_y]
    endpos = [random.choice(r_width),random.choice(r_height)]
    while True:
        if [temp_x, temp_y] == endpos:
            endpos = [random.choice(r_width),random.choice(r_height)]
        else:
            break

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
    #temptwo = numpy.full((height, width), -1, dtype=int)
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

    #mines = [[2,2],[3,2],[4,2],[5,2],[6,2],[6,3],[6,4],[6,6],[5,6],[4,6],[3,6],[2,6],[2,5],[2,4],[2,3]]
    # first record(iteration 0)
    temptwo[endpos[1]][endpos[0]] = 100
    records.append(temptwo)

if __name__ == '__main__':
    main(sys.argv[1:])
    Q_learn()
    optimal()

    anim, fig, ax = generateAnimat(records, startpos, endpos, mines=mines, opt_pol=opt,
                                   start_val=-10, end_val=100, mine_val=150, just_vals=False, generate_gif=False,
                                   vmin=-10, vmax=150)
    plt.show()