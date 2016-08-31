from TicTacToe import *
from Player import *
#import time
board = TTTBoard()
#start = time.time()
print "========MINIMAX====5===================="
board.hostGame(Player(1, Player.MINIMAX,5),Player(2, Player.MINIMAX,5))
print "========================================"
print "\n\n"
board = TTTBoard()
print "========ABPRUNE====5===================="
board.hostGame(Player(1, Player.ABPRUNE,5),Player(2, Player.ABPRUNE,5))
print "========================================"
#end = time.time()
#print "execution time: ", (end - start)
