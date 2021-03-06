# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, math

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = currentGameState.getFood().asList()

        negMinDistToFood = 0

        if len(foodList) == 0:
          negMinDistToFood = 0
        else:
          negMinDistToFood = -min([manhattanDistance(newPos, dot) for dot in foodList])

        ghostPanic = 0

        for ghost in newGhostStates:
          if ghost.scaredTimer == 0 and manhattanDistance(newPos, ghost.getPosition()) <= 2:
            #if a nonscared ghost is <= 2 moves away
            ghostPanic = -100
        
        # compute the "slack time" that pacman has to get to each scared ghost, i.e. scared time - ghost distance (if positive)
        # sum up slack times
        pursueGhosts = 0 if len(newGhostStates) == 0 else sum([ max(0, ghost.scaredTimer - manhattanDistance(newPos, ghost.getPosition())) for ghost in newGhostStates])



        return negMinDistToFood + ghostPanic + pursueGhosts

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        return self.maxValueActionPair(gameState, self.depth)[1]

    def maxValueActionPair(self, gameState, depthRemaining):
      actions = gameState.getLegalActions(0) 

      if depthRemaining == 0 or len(actions) == 0: 
        return (self.evaluationFunction(gameState), None)

      val = float('-inf')
      bestAction = None

      # 0 in getLegalActions(0) because pacman has index 0
      for action in actions:
        newVal = self.minValue(gameState.generateSuccessor(0, action), depthRemaining, 1)
        if val < newVal:
          val = newVal
          bestAction = action

      return (val,bestAction)

    def minValue(self, gameState, depthRemaining, agentIndex):
      actions = gameState.getLegalActions(agentIndex)

      if len(actions) == 0:
        return self.evaluationFunction(gameState)

      val = float('inf')

      if agentIndex == gameState.getNumAgents() - 1:
        # looking at the last adversary (ghost), return to max agent (pacman)


        for action in actions:
          val = min(val, self.maxValueActionPair(gameState.generateSuccessor(agentIndex, action), depthRemaining - 1)[0])

      else:
        # more adversaries (ghosts) remain

        for action in actions:
          val = min(val, self.minValue(gameState.generateSuccessor(agentIndex,action), depthRemaining, agentIndex + 1))

      return val


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.maxValueActionPair(gameState, self.depth, float('-inf'), float('inf'))[1]

    def maxValueActionPair(self, gameState, depthRemaining, alpha, beta):
      actions = gameState.getLegalActions(0) 

      if depthRemaining == 0 or len(actions) == 0:
        return (self.evaluationFunction(gameState), None)

      val = float('-inf')
      bestAction = None

      # 0 in getLegalActions(0) because pacman has index 0
      for action in actions:
        newVal = self.minValue(gameState.generateSuccessor(0, action), depthRemaining, 1, alpha, beta)
        if val < newVal:
          val = newVal
          bestAction = action

          if val > beta: return (val, bestAction)
          alpha = max(alpha,val)

      return (val,bestAction)

    def minValue(self, gameState, depthRemaining, agentIndex, alpha, beta):
      actions = gameState.getLegalActions(agentIndex)

      if len(actions) == 0:
        return self.evaluationFunction(gameState)

      val = float('inf')

      if agentIndex == gameState.getNumAgents() - 1:
        # looking at the last adversary (ghost), return to max agent (pacman)

        for action in actions:
          val = min(val, self.maxValueActionPair(gameState.generateSuccessor(agentIndex, action), depthRemaining - 1, alpha, beta)[0])
          if val < alpha: return val
          beta = min(beta,val)

      else:
        # more adversaries (ghosts) remain

        for action in actions:
          val = min(val, self.minValue(gameState.generateSuccessor(agentIndex,action), depthRemaining, agentIndex + 1, alpha, beta))
          if val < alpha: return val
          beta = min(beta,val)

      return val

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.maxValueActionPair(gameState, self.depth)[1]

    def maxValueActionPair(self, gameState, depthRemaining):
      actions = gameState.getLegalActions(0) 

      if depthRemaining == 0 or len(actions) == 0: 
        return (self.evaluationFunction(gameState), None)

      val = float('-inf')
      bestAction = None

      # 0 in getLegalActions(0) because pacman has index 0
      for action in actions:
        newVal = self.expAdvValue(gameState.generateSuccessor(0, action), depthRemaining, 1)
        if val < newVal:
          val = newVal
          bestAction = action

      return (val,bestAction)

    # Expected value from adversarial move
    def expAdvValue(self, gameState, depthRemaining, agentIndex):
      actions = gameState.getLegalActions(agentIndex)
      numActions = float(len(actions))

      if len(actions) == 0:
        return self.evaluationFunction(gameState)

      expVal = 0

      if agentIndex == gameState.getNumAgents() - 1:
        # looking at the last adversary (ghost), return to max agent (pacman)


        for action in actions:
          expVal += self.maxValueActionPair(gameState.generateSuccessor(agentIndex, action), depthRemaining - 1)[0]

      else:
        # more adversaries (ghosts) remain

        for action in actions:
          expVal += self.expAdvValue(gameState.generateSuccessor(agentIndex,action), depthRemaining, agentIndex + 1)

      expVal = float(expVal) / float(len(actions))

      return expVal

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    pacPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()

    md = util.manhattanDistance


    # FEATURE: discount gameState if a nonscared ghost is close
    ghostPanic = -500 if min(4, [md(pacPos,ghost.getPosition()) for ghost in ghostStates if ghost.scaredTimer <= 0]) <= 3 else 0

    # FEATURE: for every scared ghost, add the "head start" pacman has on the ghost, i.e. scaredTime - distance to ghost
    pursueGhosts = sum([max(0, ghost.scaredTimer - md(pacPos,ghost.getPosition())) for ghost in ghostStates])

    foodList = currentGameState.getFood().asList()

    # FEATURE: proximity to food (in aggregate) times 500, i.e. 500 * (sum of distances to food)^-1
    # use 1000 if no food
    foodProximity = 1000 if len(foodList) == 0 else 500.0 / sum([md(pacPos, dot) for dot in foodList])

    # FEATURE: score of game
    score = currentGameState.getScore()

    import random

    # sum features and add a little randomness to help pacman out of ruts

    return score + foodProximity + pursueGhosts + ghostPanic + random.randint(0,1)

# Abbreviation
better = betterEvaluationFunction

