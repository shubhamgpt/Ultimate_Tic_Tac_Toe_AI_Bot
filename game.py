import sys
import random
import signal
import minmaxai
import randomai
# handle timer

class TimedOutExc(Exception):
        pass

def handler(signum, frame):
    raise TimedOutExc()


class ManualPlayer:
	def __init__(self):
		pass
	def move(self, tempBoard, tempBlock, oldMove, flag):
		print 'Enter your move: (row column) (you\'re playing with', flag + ")"
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))



#Game Initilization
def getStatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)

	BlockState = ['-']*9
	return board, BlockState

# Checks if player has cheated. Don't mess with the board.
def boardVerify(gameBoard, tempBoardState):
	return gameBoard == tempBoardState

# Player cheated. Don't mess with the Block.
def BlockVerify(BlockState, tempBlockState):
	return BlockState == tempBlockState

#Empty cells from valid blocks.
def getAllEmpty(gameb, blal,BlockState):
	cells = []  # it will be list of tuples
	#Loop and find blocks and empty cells.
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# Free to play move anywhere if all blocks are full.
	if cells == []:
		for i in range(9):
			for j in range(9):
                                no = (i/3)*3
                                no += (j/3)
				if gameb[i][j] == '-' and BlockState[no] == '-':
					cells.append((i,j))
	return cells

# Won blocks are not abandoned but, no point in playing in them.
# If move is valid, return true.
def validMove(gameBoard,BlockState, curMove, oldMove):

	# Check if curMove is a tuple or not.
	# oldMove is always correct.
	if type(curMove) is not tuple:
		return False

	if len(curMove) != 2:
		return False

	a = curMove[0]
	b = curMove[1]

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#At the start of the game, any move is ok.
	if oldMove[0] == -1 and oldMove[1] == -1:
		return True


	forCorner = [0,2,3,5,6,8]

	#List of next valid blocks.
	allowedBlocks  = []

	if oldMove[0] in forCorner and oldMove[1] in forCorner:
		## Can chose from 3 adjacent blocks.

		if oldMove[0] % 3 == 0 and oldMove[1] % 3 == 0:
			## top left 3 Blocks are allowed
			allowedBlocks = [0,1,3]
		elif oldMove[0] % 3 == 0 and oldMove[1] in [2,5,8]:
			## top right 3 Blocks are allowed
			allowedBlocks = [1,2,5]
		elif oldMove[0] in [2,5,8] and oldMove[1] % 3 == 0:
			## bottom left 3 Blocks are allowed
			allowedBlocks  = [3,6,7]
		elif oldMove[0] in [2,5,8] and oldMove[1] in [2,5,8]:
			### bottom right 3 Blocks are allowed
			allowedBlocks = [5,7,8]

		else:
			print "Game crashed!"
			sys.exit(1)

	else:
		#### Can chose only from 1 adjacent block. If none, free to play anywhere on board.
		if oldMove[0] % 3 == 0 and oldMove[1] in [1,4,7]:
			## Allowed upper-center Block
			allowedBlocks = [1]

		elif oldMove[0] in [1,4,7] and oldMove[1] % 3 == 0:
			## Allowed middle-left Block
			allowedBlocks = [3]

		elif oldMove[0] in [2,5,8] and oldMove[1] in [1,4,7]:
			## Alowed lower-center Block
			allowedBlocks = [7]

		elif oldMove[0] in [1,4,7] and oldMove[1] in [2,5,8]:
			## Allowed middle-right Block
			allowedBlocks = [5]

		elif oldMove[0] in [1,4,7] and oldMove[1] in [1,4,7]:
			allowedBlocks = [4]

        #If block is won by a player, player cannot move there.

        for i in reversed(allowedBlocks):
            if BlockState[i] != '-':
                allowedBlocks.remove(i)

        # Empty cells in allowed blocks. If full, al empty cells in the board are valid moves.
        cells = getAllEmpty(gameBoard, allowedBlocks,BlockState)

	#Is this a valid move?.
        if curMove in cells:
     	    return True
        else:
    	    return False

def listsUpdate(gameBoard, BlockState, tentativeMove, fl):
	#tentativeMove contains move to be made. Modify game board and then check if BlockState needs to be modified.
	gameBoard[tentativeMove[0]][tentativeMove[1]] = fl

	blockNumber = (tentativeMove[0]/3)*3 + tentativeMove[1]/3
	id1 = blockNumber/3
	id2 = blockNumber%3
	mg = 0
	mflg = 0
	if BlockState[blockNumber] == '-':
		if gameBoard[id1*3][id2*3] == gameBoard[id1*3+1][id2*3+1] and gameBoard[id1*3+1][id2*3+1] == gameBoard[id1*3+2][id2*3+2] and gameBoard[id1*3+1][id2*3+1] != '-':
			mflg=1
		if gameBoard[id1*3+2][id2*3] == gameBoard[id1*3+1][id2*3+1] and gameBoard[id1*3+1][id2*3+1] == gameBoard[id1*3][id2*3 + 2] and gameBoard[id1*3+1][id2*3+1] != '-':
			mflg=1

                if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if gameBoard[id1*3][i]==gameBoard[id1*3+1][i] and gameBoard[id1*3+1][i] == gameBoard[id1*3+2][i] and gameBoard[id1*3][i] != '-':
                                mflg = 1
                                break

                ### row-wise
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if gameBoard[i][id2*3]==gameBoard[i][id2*3+1] and gameBoard[i][id2*3+1] == gameBoard[i][id2*3+2] and gameBoard[i][id2*3] != '-':
                                mflg = 1
                                break


	if mflg == 1:
		BlockState[blockNumber] = fl

        #check for draw on the Block.

        id1 = blockNumber/3
	id2 = blockNumber%3
        cells = []
	for i in range(id1*3,id1*3+3):
	    for j in range(id2*3,id2*3+3):
		if gameBoard[i][j] == '-':
		    cells.append((i,j))

        if cells == [] and mflg!=1:
            BlockState[blockNumber] = 'd' #Draw

        return

def endGame(gameBoard, BlockState):

        #Check if game is won by any player.
        bs = BlockState
	## Row which win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		#print Blockstate
		return True, 'W'
	## Col which win
	elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
		#print Blockstate
		return True, 'W'
	## Diag which win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
		#print Blockstate
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			for j in range(9):
				if gameBoard[i][j] == '-' and BlockState[(i/3)*3+(j/3)] == '-':
					smfl = 1
					break
		if smfl == 1:
                        #Game continues!
			return False, 'Continue'

		else:
                        #Change in scoring mechanism
                        # 1. If game is tie, player with most won boxes, wins.
                        # 2. If number of boxes won is also same,player with more corner moves, wins.
                        point1 = 0
                        point2 = 0
                        for i in BlockState:
                            if i == 'x':
                                point1+=1
                            elif i=='o':
                                point2+=1
			if point1>point2:
				return True, 'Player1'
			elif point2>point1:
				return True, 'Player2'
			else:
                                point1 = 0
                                point2 = 0
                                for i in range(len(gameBoard)):
                                    for j in range(len(gameBoard[i])):
                                        if i%3!=1 and j%3!=1:
                                            if gameBoard[i][j] == 'x':
                                                point1+=1
                                            elif gameBoard[i][j]=='o':
                                                point2+=1
			        if point1>point2:
				    return True, 'Player1'
			        elif point2>point1:
				    return True, 'Player2'
                                else:
				    return True, 'D'


def decideWin(player,status, message):
	if player == 'Player1' and status == 'L':
		return ('Player2',message)
	elif player == 'Player1' and status == 'W':
		return ('Player1',message)
	elif player == 'Player2' and status == 'L':
		return ('Player1',message)
	elif player == 'Player2' and status == 'W':
		return ('Player2',message)
	else:
		return ('NO ONE','DRAW')
	return


def displayBoard(gb, bs):
	print '____ Game Board ____'
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + {"x":"X","o":"O","-":"_"}[gb[i][j]],
			else:
				print {"x":"X","o":"O","-":"_"}[gb[i][j]],

		print
	print "____________________\n"

	print "__ Overall Board __"
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2]
	print "___________________"
	print


def simulate(obj1,obj2):

	# Game board is a 9x9 list, BlockState is a 1 Dimension list of 9 elements
	gameBoard, BlockState = getStatus()

	pl1 = obj1
	pl2 = obj2

	### Player with 'x' symbol starts first.
	Player1Flag = 'x'
	Player2Flag = 'o'

	oldMove = (-1, -1) # First move

	WINNER = ''
	MESSAGE = ''

    #Time limit = 6 seconds.
	TIMEALLOWED = 6000

	displayBoard(gameBoard, BlockState)

	while(1):
		# Player1's move
		tempBoardState = gameBoard[:]
		tempBlockState = BlockState[:]
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		# Player1 needsd to complete in the time limit.
		try:
			getPlayer1Move = pl1.move(tempBoardState, tempBlockState, oldMove, Player1Flag)
		except TimedOutExc as e:
			WINNER, MESSAGE = decideWin('Player1', 'L',   'TIMED OUT')
			break
		signal.alarm(0)

                #Check if player is cheating.Do not make changes in list.
		if not (boardVerify(gameBoard, tempBoardState) and BlockVerify(BlockState, tempBlockState)):
			#If modified, player 1 loses.
			WINNER, MESSAGE = decideWin('Player1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break

		# Is move valid?
		if not validMove(gameBoard, BlockState,getPlayer1Move, oldMove):
			## If player makes wrong move, Player loses.
			WINNER, MESSAGE = decideWin('Player1', 'L',   'MADE AN INVALID MOVE')
			break


		print "Player 1 made the move:", getPlayer1Move, 'with', Player1Flag

                #Update gameBoard and BlockState if move is valid.
                listsUpdate(gameBoard, BlockState, getPlayer1Move, Player1Flag)

		# Checking if the last move resulted in a terminal state
		gamestatus, mesg =  endGame(gameBoard, BlockState)
		if gamestatus == True:
			displayBoard(gameBoard, BlockState)
			WINNER, MESSAGE = decideWin('Player1', mesg,  'COMPLETE')
			break


		oldMove = getPlayer1Move
		displayBoard(gameBoard, BlockState)

                # Player2's turn

                tempBoardState = gameBoard[:]
                tempBlockState = BlockState[:]


		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		try:
                	getPlayer2Move = pl2.move(tempBoardState, tempBlockState, oldMove, Player2Flag)
		except TimedOutExc as e:
			WINNER, MESSAGE = decideWin('Player2', 'L',   'TIME OUT')
			break
		signal.alarm(0)

                if not (boardVerify(gameBoard, tempBoardState) and BlockVerify(BlockState, tempBlockState)):
			WINNER, MESSAGE = decideWin('Player2', 'L',   'MODIFIEDENVIRONMENT')
			break

                if not validMove(gameBoard, BlockState,getPlayer2Move, oldMove):
			WINNER, MESSAGE = decideWin('Player2', 'L',   'INVALID MOVE')
			break


		print "Player 2 made the move:", getPlayer2Move, 'with', Player2Flag

                listsUpdate(gameBoard, BlockState, getPlayer2Move, Player2Flag)

		gamestatus, mesg =  endGame(gameBoard, BlockState)
                if gamestatus == True:
			displayBoard(gameBoard, BlockState)
                        WINNER, MESSAGE = decideWin('Player2', mesg,  'COMPLETE' )
                        break
		oldMove = getPlayer2Move
		displayBoard(gameBoard, BlockState)

	print WINNER + " won!"
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	if len(sys.argv) != 2:
		print 'How to: python game.py <game_mode>'
		print '<game_mode> can be 1 => Random player vs. Random player'
		print '                   2 => Human vs. Random Player'
		print '                   3 => Human vs. Human'
		sys.exit(1)

	obj1 = ''
	obj2 = ''
	option = sys.argv[1]
	if option == '1':
		obj1 = minmaxai.AI()
		obj2 = randomai.AI()

	elif option == '2':
		obj1 = minmaxai.AI()
		obj2 = ManualPlayer()

	elif option == '3':
		obj1 = ManualPlayer()
		obj2 = ManualPlayer()

        # Coin toss to decide player 1 and player 2.
        # But in a tournament each player will get to go first.
        num = random.uniform(0,1)
        if num > 0.5:
		simulate(obj2, obj1)
	else:
		simulate(obj1, obj2)
