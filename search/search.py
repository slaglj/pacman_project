# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class stateWithPathData:
    """
    Student added class (Jake Slagle)

    
    A stateWithPathData is a state in a search problem with added data pertaining to
    that state in the context of executing a search problem, specifically:

        prevMetaState: the state (with path data) from which this state was arrived at
        action: the action takent to get from prevMetaState to state
        costToState: the cost of the path taken to reach this state

    Including this class accomplishes two things to help execute the algorithm:

    (1) Allows us to reconstruct the path once the goal state is reached by accesseing prevMetaState,
        for all search algorithms (we are essentially creating an implicit linked list)
    (2) Allows us to quickly evaluate the cost of the path up to this state with costToState() for
        uniform cost search and A* search
    """

    def __init__(self, state, prevMetaState, action, costToState):
        self.state = state
        self.prevMetaState = prevMetaState
        self.action = action
        self.costToState = costToState

    def getState(self):
        return self.state

    def getPrevMetaState(self):
        return self.prevMetaState

    def getAction(self):
        return self.action 

    def getCostToState(self):
        return self.costToState


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def graphSearch(problem, fringe):
    """
    visitedStates = set(problem.getStartState())
    currMetaState = stateWithPathData(problem.getStartState(), None, None, 0)

    # Do Graph search while maintaining backpointers. Note that any given state will only have its
    # back pointer set at most once
    while(not problem.isGoalState(currMetaState.getState())):
        currState = currMetaState.getState()

        for (nextState, action, cost) in problem.getSuccessors(currState):
            if nextState not in visitedStates:
                fringe.push(stateWithPathData(nextState, currMetaState, action, currMetaState.getCostToState() + cost))
                visitedStates.add(nextState)
            

        if fringe.isEmpty(): return []
        currMetaState = fringe.pop()
    
    """
    visitedStates = set()
    fringe.push(stateWithPathData(problem.getStartState(), None, None, 0))

    reachedGoal = False
    # Do Graph search while maintaining backpointers. Note that any given state will only have its
    # back pointer set at most once
    while(not reachedGoal):
        if fringe.isEmpty(): return []

        currMetaState = fringe.pop()
        currState = currMetaState.getState()

        if problem.isGoalState(currState):
            reachedGoal = True
        elif currState not in visitedStates:
            visitedStates.add(currState)
            for (nextState, action, cost) in problem.getSuccessors(currState):
                if nextState not in visitedStates:
                    fringe.push(stateWithPathData(nextState, currMetaState, action, currMetaState.getCostToState() + cost))
    
    solution = []

    while(currMetaState.getPrevMetaState() != None): 
        solution.append(currMetaState.getAction())
        currMetaState = currMetaState.getPrevMetaState()

    solution.reverse()
    return solution

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    """

    from util import Stack
    return graphSearch(problem, Stack())

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue
    return graphSearch(problem, Queue())

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    from util import PriorityQueueWithFunction
    return graphSearch(problem, PriorityQueueWithFunction(lambda item: item.getCostToState()))

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    from util import PriorityQueueWithFunction
    return graphSearch(problem, PriorityQueueWithFunction(lambda item: item.getCostToState() + heuristic(item.getState(), problem)))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
