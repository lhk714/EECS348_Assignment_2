# File: hlg483.py
# Author(s) names AND netid's: Haikun Liu    hlg483
# Date: 04.22.2016
# Statement: I worked individually on this project and all work is my own.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *
import time
import math

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4

    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)

    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score

    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY  # note value
        alpha = -INFINITY  # worst MAX value
        beta = INFINITY  #worst MIN value
        turn = self
        for m in board.legalMoves(self):
            # for each legal move
            if ply == 0:
                # if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            # make a new board
            nb.makeMove(self, m)
            # try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.alphaBetaMinValue(nb, ply - 1, turn, alpha, beta)
            # and see what the opponent would do next
            if s > score:
                # if the result is better than our best score so far, save that move,score
                move = m
                score = s
        # return the best score and move so far
        return score, move

    def alphaBetaMaxValue(self,board,ply,turn,alpha,beta):
        """ Find the value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY  #worst score for MAX

        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.alphaBetaMinValue(nextBoard, ply - 1, turn, alpha, beta)
            # print "s in maxValue is: " + str(s)
            score = max(score,s)  #if the result s is better than score, set score = s
            if score > beta:  #terminate the branch, if score is greater than beta (optimal MAX)
                return score
            alpha = max(alpha,score)
        return score

    def alphaBetaMinValue(self, board, ply, turn, alpha, beta):
        """ Find the value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY  #worst score for MIN
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.alphaBetaMaxValue(nextBoard, ply - 1, turn, alpha, beta)
            # print "s in maxValue is: " + str(s)
            score = min(score,s)  #if the result s is worse than socre, set socre = s
            if score < alpha:  #terminate the branch, if score is less than alpha (optimal MIN)
                return score
            beta = min(beta, score)  #update beta for a smaller value, if possible
        return score


    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            """using timer to adjust ply. The idea is that:
             The branching factor b of the Mancala game is 6
             The time complexity of find a move is close to depth first search O(b^m)
             The approximate time used to make a move is alpha*(b^m), where the depth m is ply
             The factor alpha can be found by counting the time of making the FIRST move with ply = 3 initially
             The maximum time allowed for a move is 10s
             We can update ply to a optimal value by ply = log(10/alpha)/log(6)
             After finding the optimized ply, we can fix it for the following moves
            """
            if self.plyFlag==True:  #It is the first move, we can use a timer to count the time used to make that move with initial ply
                startTime = time.time()  # start the timer
                val, move = self.myMove(board, self.ply)  # make a move
                endTime = time.time()  # stop the timer
                alpha = (endTime-startTime)/(math.pow(6,self.ply))  # calculate factor alpha
                ply =int(math.ceil(math.log(10/alpha,6)))  #optimized ply
                self.helpChangePly(ply,False)  #update ply, and fix ply for future moves
            else:  #optimize ply is set for future moves
                #startTime = time.time()
                val, move = self.myMove(board, self.ply)
                #endTime = time.time()
                #print "ply=", self.ply," timeDiff=", (endTime-startTime)
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class hlg483(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, playerNum, playerType, ply=3):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply
        self.plyFlag = True  #a flag used to change ply. If it is Ture, ply can be updated

    def helpChangePly(self,ply,plyFlag):
        """Upate ply"""
        self.ply = ply
        self.plyFlag = plyFlag


    def score(self, board):
        """ The idea of this customized score() function is to keep as many stones as possible at your side
        and as few stones as possible at your opponent's side"""

        numOfStone = sum(board.P1Cups) + sum(board.P2Cups) + sum(board.scoreCups)  #get the total number of stones from the board, =48

        if self.num == 1:
            if board.scoreCups[0] > numOfStone/2:  #check if the number of stones in your mancala is larger than half of the stones
                return float(numOfStone)  #return the total number of stones as score, =48
            elif board.scoreCups[1] > numOfStone/2: #if the number of stones in your opponent's mancala is larger than half of the stones
                return -float(numOfStone)  #return the negative value of total number of stones as score, =-48
            else:
                return float(sum(board.P1Cups) - sum(board.P2Cups) + board.scoreCups[0] - board.scoreCups[1])  #the current score = number of stone at your side - number of stone ar your opponent's side
        else:
            if board.scoreCups[1] > numOfStone / 2:  #check if the number of stones in your mancala is larger than half of the stones
                return float(numOfStone)  #return the total number of stones as score, =48
            elif board.scoreCups[0] > numOfStone / 2:  #if the number of stones in your opponent's mancala is larger than half of the stones
                return -float(numOfStone)   #return the negative value of total number of stones as score, =-48
            else:
                return float(sum(board.P2Cups) - sum(board.P1Cups) + board.scoreCups[1] - board.scoreCups[0])  #the current score = number of stone at your side - number of stone ar your opponent's side

    def myMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move)
         players will get extra turns when they land in their own Mancalas with their last stones"""
        move = -1
        score = -INFINITY  # note value
        alpha = -INFINITY  # worst MAX value
        beta = INFINITY  # worst MIN value
        turn = self
        for m in board.legalMoves(self):
            # for each legal move
            if ply == 0:
                # if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)   # make a new board
            if nb.makeMove(self, m):  # check if the player gets a extra move, if Ture, then the player earns a extra move
                my = hlg483(self.num, self.type, self.ply)  # make a new player to play the own side
                s = my.myMaxValue(nb, ply - 1, turn, alpha, beta)  #repeat myMaxValue() here, because the objective of the player is to obtain a higher score, which matches to the initial move
            else:  # if there is no extra move
                # try the move
                opp = hlg483(self.opp, self.type, self.ply)  # make a new player to play the opponent side
                s = opp.myMinValue(nb, ply - 1, turn, alpha, beta)
            # and see what the opponent would do next
            if s > score:
                # if the result is better than our best score so far, save that move,score
                move = m
                score = s
        # return the best score and move so far
        return score, move

    def myMaxValue(self, board, ply, turn, alpha, beta):
        """ Find the value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY  # worst score for MAX
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            nextBoard = deepcopy(board)  # Copy the board so that we don't ruin it
            if nextBoard.makeMove(self, m):  # check if the player gets a extra move, if Ture, then the player earns a extra move
                myself = hlg483(self.num, self.type, self.ply)  # make a new player to play the own side
                s = myself.myMaxValue(nextBoard, ply - 1, turn, alpha, beta)  # repeat if the player gets a extra turn
            else:
                opponent = hlg483(self.opp, self.type, self.ply)  # make a new player to play the other side
                s = opponent.myMinValue(nextBoard, ply - 1, turn, alpha, beta)
            # print "s in maxValue is: " + str(s)
            score = max(score, s)  # if the result s is better than score, set score = s
            if score > beta:  # terminate the branch, if score is greater than beta (optimal MAX)
                return score
            alpha = max(alpha, score)
        return score

    def myMinValue(self, board, ply, turn, alpha, beta):
        """ Find the value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY  # worst score for MIN
        for m in board.legalMoves(self):
            if ply == 0:
                # print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            nextBoard = deepcopy(board)# Copy the board so that we don't ruin it
            if nextBoard.makeMove(self, m):  # check if the player gets a extra move, if Ture, then the player earns a extra move
                myself = hlg483(self.num, self.type, self.ply)# make a new player to play the own side
                s = myself.myMinValue(nextBoard, ply - 1, turn, alpha, beta) # repeat if the player gets a extra turn
            else:
                opponent = hlg483(self.opp, self.type, self.ply)# make a new player to play the other side
                s = opponent.myMaxValue(nextBoard, ply - 1, turn, alpha, beta)
            # print "s in maxValue is: " + str(s)
            score = min(score, s)  # if the result s is worse than socre, set socre = s
            if score < alpha:  # terminate the branch, if score is less than alpha (optimal MIN)
                return score
            beta = min(beta, score)  # update beta for a smaller value, if possible
        return score

