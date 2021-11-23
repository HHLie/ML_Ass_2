CSC3022F
ML Assignment 2
LXXHSI007

_________________________________________________________________________________________________________
Files:

ValueIteration.py -
Computes each states value of the grid(given the width and height parameters) by
 using the Value Iteration algorithm, then an optimal path is found. The final
 Iterations and path will be shown using the generateAnimat() method from Animate.py



QLearning.py -
Computes each visited states' value of the grid(given the width and height parameters) by
 using the Q Learning algorithm, then an optimal path is found. 
The Q learning algorithm uses a decaying e-greedy value, 
which determines the probility of taking either a random action or the best possible action.
 The Iterations and path will be shown using the generateAnimat() method from Animate.py

Animate.py -
Handles and creates the graphic to show the Iterations, or epochs of each algorithm


Makefile -
A simple makefile with the following commands;
install:
  Installs all packages specified in the requirements.txt file into the virtual environment.

venv:
  Check if there is a virtual environment called venv in directory, if there isn't one present create one.

clean:
  Remove the virtual environment and delete all .pyc files.

_________________________________________________________________________________________________________
Running the program:
Use "make install" or "make venv" to create the virtual environment.

Part 1: Value Iteration

python ValueIteration.py width height [options]

The available options are:
• -start xpos ypos which specifies the starting location of the agent.(default is random)
• -end xpos ypos which specifies the target destination of the agent.(default is random)
• -k num which specifies the number of landmines that should be randomly placed
within the environment.(default to 3)
• -gamma g which specifies the discount factor of the agent. (Set to 0.8 for default)

Part 2: Q-Learning

python QLearning.py width height [options]

The available options are:
• -start xpos ypos which specifies the starting location of the agent at the beginning
of every epoch.(default is random)
• -end xpos ypos which specifies the target destination of the agent.(default is random)
• -k num which specifies the number of landmines that should be randomly placed
within the environment.(default to 3)
• -gamma g which specifies the discount factor of the agent.(default to a 0.8)
• -learning n which specifies the learning rate of the agent.(default to 0.4)
• -epochs e which specifies how many episodes your agent should learn for.(default to 500)


_________________________________________________________________________________________________________
