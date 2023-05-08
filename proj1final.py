#Name: Milind Devnani
#netID: mdevn001
#student ID: 862134795
# Perform necessary imports

import math
import queue
from queue import PriorityQueue
import copy

# Define parameters
global DesieredState
global ProblemSize
global RootSizePlusOne

frontier = PriorityQueue()
nodesVisited = []

#making the node class:
class Node:
    def __init__(self, state) -> None:
        self.pathCost = 0
        self.heuristicCost = 0
        self.state = state

    def getCost(self):
        return self.pathCost + self.heuristicCost

    def __lt__(self, compareNode):
        return self.getCost() < compareNode.getCost()

def getProblemSize():
    global RootSizePlusOne
    ProblemSize = input("Enter Problem Size - 3, 8, 15, 24: ")
    RootSizePlusOne = math.sqrt(int(ProblemSize)+1)
    if (RootSizePlusOne/int(RootSizePlusOne) !=1) or RootSizePlusOne <=1 or RootSizePlusOne>=5:
        print("Wrong Problem Size Try Again")
        getProblemSize()

def setDesieredState():
    size = int(RootSizePlusOne)
    global DesieredState
    DesieredState = [[(j*size+i+1) for i in range(size)] for j in range(size)]
    DesieredState[size-1][size-1]=0

def printState(state):
    print("\n".join(  [ "[" + str(','.join([str(i) for i in j]) +']'  ) for j in state]))

def getInitialState():
    size = int(RootSizePlusOne)
    choiceRemaining = [i for i in range(size*size)]
    state = [[0 for i in range(size)] for j in range(size)]
    printState(state)
    def setStateValue(i):
        n = input("Enter number at position " + str(i) + " select from " + str(choiceRemaining) + " spot(Use 0 as the empty space) ")
        try:
            choiceRemaining.remove(int(n))
            state[(i-1)//size][(i-1)%size] = int(n)
        except:
            print('Selected Number Not In Choice List. Try Again')
            setStateValue(i)
    for i in range(1,size*size+1):
        setStateValue(i)
        printState(state)
    return state

def stateAsDict(state):
    size = int(RootSizePlusOne)
    d = {}
    for i in range(size):
        for j in range(size):
            d[state[i][j]] = (i,j)
    return d

def dictAsState(d):
    size = int(RootSizePlusOne)
    state = [[0 for i in range(size)] for j in range(size)]
    for key in d:
        state[d[key][0]][d[key][1]] = key
    return state

def getHeuristicOption():
    print("Select Heuristic Option")
    print("1: Uniform Cost Search - 0 Heuristic cost")
    print("2: A* with Misplaced Tile Heuristic cost")
    print("3: A* with Manhattan Distance Heuristic cost")
    heuristicOption = input("Choose an algorithm ")
    if heuristicOption not in ('1', '2', '3'):
        print('Not a Valid Option. Try Again')
    return int(heuristicOption)

# Define function to get cost of Heuristic options
def getHeuristicCost(node, heuristicOption):
    size = int(RootSizePlusOne)
    # Uniform Heuristic Cost
    if heuristicOption == 1:
        return 0
    # Misplaced Heuristic Cost
    elif heuristicOption == 2:
        cost = 0
        for i in range(size*size):
            if (node.state)[i//size][i%size] != DesieredState[i//size][i%size]:
                cost+=1
        return cost
    # Manhattan Distance Heuristc Cost
    elif heuristicOption == 3:
        stateIndex = stateAsDict(node.state)
        desieredIndex = stateAsDict(DesieredState)
        cost = 0
        for key in desieredIndex:
            cost = cost + abs(desieredIndex[key][0]-stateIndex[key][0]) + abs(desieredIndex[key][1]-stateIndex[key][1])
        return cost

def isValidIndex(index):
    size = int(RootSizePlusOne)
    if index[0]<0 or index[0]>=size or index[1]<0 or index[1]>=size:
        return False
    else:
        return True

def action(node, heuristic):
    #There are for possible actions. Some nodes can take limited actions
    nodeList = []
    state = node.state
    stateIndex = stateAsDict(state)
    zeroIndex = stateIndex[0]

    def moveZero(newIndex):
        newState = copy.deepcopy(state)
        value = newState[newIndex[0]][newIndex[1]]
        newState[newIndex[0]][newIndex[1]] = 0
        newState[zeroIndex[0]][zeroIndex[1]] = value
        newNode = Node(newState)
        newNode.pathCost = node.pathCost + 1
        newNode.heuristicCost = getHeuristicCost(newNode, heuristic)
        return newNode

    # Move up:
    cellAboveZeroIndex = (zeroIndex[0]-1, zeroIndex[1])
    if isValidIndex(cellAboveZeroIndex):
        newNode = moveZero(cellAboveZeroIndex)
        nodeList.append(newNode)
    else:
        # move not allowed. do nothing
        None

    # Move down:
    cellBelowZeroIndex = (zeroIndex[0]+1, zeroIndex[1])
    if isValidIndex(cellBelowZeroIndex):
        newNode = moveZero(cellBelowZeroIndex)
        nodeList.append(newNode)
    else:
        # move not allowed. do nothing
        None

    # Move left:
    cellLeftOfZeroIndex = (zeroIndex[0], zeroIndex[1]-1)
    if isValidIndex(cellLeftOfZeroIndex):
        newNode = moveZero(cellLeftOfZeroIndex)
        nodeList.append(newNode)
    else:
        # move not allowed. do nothing
        None

    # Move right:
    cellRightOfZeroIndex = (zeroIndex[0], zeroIndex[1]+1)
    if isValidIndex(cellRightOfZeroIndex):
        newNode = moveZero(cellRightOfZeroIndex)
        nodeList.append(newNode)
    else:
        # move not allowed. do nothing
        None

    return nodeList

#uniform cost search is a star with heuristic set to 0
def aStar(heuristicChoice):
    # Initially our queue size is 1 representing the InitialState state or node
    maxSizeQueue = 1
    # We will expand the InitialState node
    expandedNodes = 1
    if(heuristicChoice in (1,2,3)):
        while not frontier.empty():
            node = frontier.get()
            if node.state == DesieredState:
                print("Goal state!")
                print("Solution depth was: " + str(node.pathCost))
                print("Number of nodes expanded: " + str(expandedNodes))
                print("Max queue size: "  + str(maxSizeQueue))
                return True
            if node.state not in nodesVisited:
                print("The best state to expand with g(n) = "+ str(node.pathCost) + " and h(n) = " + str(node.heuristicCost) + " is...")
                printState(node.state)
                expandedNodes+=1
                toExpand = action(node, heuristicChoice)
                for nodesLeft in toExpand:
                    if nodesLeft.state not in nodesVisited:
                        frontier.put(nodesLeft)
                        maxSizeQueue = max(maxSizeQueue, frontier.qsize())
                nodesVisited.append(node.state)

        print("No Solution!!!") #these lines of code are kind of useless for the 8-puzzle but not for smaller puzzles, for example a puzzle with no solution where n = 3.
        print("Number of nodes expanded: " + str(expandedNodes))
        print("Max queue size: "  + str(maxSizeQueue))
        return False

    else:
        print("No option")
        exit(0)

def main():
    getProblemSize()
    setDesieredState()
    # getInitialState()
    node = Node(getInitialState())
    #print(getHeuristicCost(node, 1))
    #print(getHeuristicCost(node, 2))
    #print(getHeuristicCost(node, 3))
    #print(isValidIndex((-1,1)))
    n = action(node, 3)
    #[printState(x.state) for x in n]
    frontier.put(node)
    opt = getHeuristicOption()
    aStar(opt)

main()
