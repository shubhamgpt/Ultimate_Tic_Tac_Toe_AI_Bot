import random
import copy
import sys
class AI():

	def __init__(self):
		self.APPROX_WIN_SCORE = 7
		self.OVERALL_BOARD_WEIGHT = 23
		self.WIN_SCORE = 10**6
		self.AB_DEPTH = 3
		self.WIN_SEQ = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
		self.scoresStored = [0]*8
		self.first = 0
		self.maxxx = sys.maxint

	MAXX = sys.maxint


	def move(self, state, tempBlock, oldMove, flag):
		#print flag
		self.first = 0
		if(oldMove[0] == -1 and oldMove[1] == -1):
			return (4,4)
		actions = []
		choiceFinal = []
		cells = []
		cells = self.legalActions(state,tempBlock,oldMove,flag)

		if type(cells) == tuple:
			y = []
			y.append(cells)
			cells = y

		if(len(cells) == 1):
			return (cells[0][0], cells[0][1])

		if (len(cells) >= 2):
			self.AB_DEPTH = 2
		else:
			self.AB_DEPTH = 3

		for act in cells:
			successorState = self.generateSuccessor(state, act, flag)
			actions.append((act, self.__min_val_ab(successorState, self.AB_DEPTH, tempBlock, flag, oldMove)))
		_, bestVal = max(actions, key=lambda x: x[1])
		choiceFinal = [bestAction for bestAction, val in actions if val == bestVal]
		i = choiceFinal[0]
		x = i[0] - (i[0]%3)
		y = i[1] - (i[1]%3)
		arr = []
		for j in [x,x+1,x+2]:
			for k in [y,y+1,y+2]:
				if state[j][k] == flag:
					arr.append(1)
				elif state[j][k] == self.op(flag):
					arr.append(-1)
				else:
					arr.append(0)
		loc = []
		for i in xrange(len(arr)):
			if arr[i] == 1:
				self.rtup(i,arr,x,y,loc)
		choiceFinal = list(set(loc).intersection(set(choiceFinal)))
		if len(choiceFinal) == 0:
			return random.choice([bestAction for bestAction, val in actions if val == bestVal])
		return random.choice(choiceFinal)

	def rtup(self, i, arr, sx, sy, x):
		for j in self.WIN_SEQ:
			if i in j:
				var = j.index(i)
				for k in xrange(len(j)):
					if k != var:
						if arr[k] == -1:
							break
						elif k == 2:
							for s in xrange(len(j)):
								if s != var:
									v1 = sx + (s/3)
									v2 = sy + (s%3)
									x.append((v1,v2))
		return

	def filter(self, tempBlock, flag):
		for i in xrange(9):
			if tempBlock[i] == flag:
				self.scoresStored[i/3] += 1
				self.scoresStored[(i%3) + 3] += 1
				if i == 0:
					self.scoresStored[6] += 1
				elif i == 2:
					self.scoresStored[7] += 1
				elif i == 4:
					self.scoresStored[6] += 1
					self.scoresStored[7] += 1
				elif i == 6:
					self.scoresStored[7] += 1
				elif i == 8:
					self.scoresStored[6] += 1
			elif tempBlock[i] != '-':
				self.scoresStored[i/3] = 0
				self.scoresStored[(i%3) + 3] = 0
				if i == 0:
					self.scoresStored[6] = 0
				elif i == 2:
					self.scoresStored[7] = 0
				elif i == 4:
					self.scoresStored[6] = 0
					self.scoresStored[7] = 0
				elif i == 6:
					self.scoresStored[7] = 0
				elif i == 8:
					self.scoresStored[6] = 0


	def func(self, index, tempBlock):

		if index == 6:
			for j in [0,4,8]:
				if tempBlock[j] == '-':
					return j

		elif index == 7:
			for j in [6,0,2]:
				if tempBlock[j] == '-':
					return j

		elif index == 1:
			for j in [4,5,3]:
				if tempBlock[j] == '-':
					return j

		elif index == 4:
			for j in [4,7,1]:
				if tempBlock[j] == '-':
					return j

		elif index == 0:
			for j in [0,1,2]:
				if tempBlock[j] == '-':
					return j

		elif index == 2:
			for j in [8,7,6]:
				if tempBlock[j] == '-':
					return j

		elif index == 3:
			for j in [6,3,0]:
				if tempBlock[j] == '-':
					return j

		elif index == 5:
			for j in [2,5,8]:
				if tempBlock[j] == '-':
					return j


	def select(self, allowedBlocks, tempBlock):
		if len(allowedBlocks) == 0:
			check = [0, 1, 2, 3, 4, 5, 6, 7]
			check = list(reversed([x for (y,x) in sorted(zip(self.scoresStored,check))]))
			for i in check:
				ret = self.func(i, tempBlock)
				if ret != None:
					return ret

		elif len(allowedBlocks) == 1:
			return allowedBlocks[0]

		else:
			maxValue = 0
			block = []
			for i in allowedBlocks:
				block.append(i/3)
				block.append((i%3)+3)
				if i == 0:
					block.append(6)
				elif i == 2:
					block.append(7)
				elif i == 4:
					block.append(6)
					block.append(7)
				elif i == 6:
					block.append(7)
				elif i == 8:
					block.append(6)

			index = block[0]
			block = list(set(block))
			for i in block:
				if self.scoresStored[i] >= maxValue:
					index = i
					maxValue = self.scoresStored[i]

			if index == 0:
				for j in list(set([1,0,2]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j

			elif index == 1:
				for j in list(set([4,3,5]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j

			elif index == 2:
				for j in list(set([7,6,8]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j

			elif index == 3:
				for j in list(set([3,6,0]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j

			elif index == 4:
				for j in list(set([4,1,7]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j

			elif index == 5:
				for j in list(set([5,2,8]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j

			elif index == 6:
				for j in list(set([4,8,0]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j

			elif index == 7:
				for j in list(set([4,2,6]).intersection(allowedBlocks)):
					if tempBlock[j] == '-':
						return j


	def legalActions(self,state,tempBlock,oldMove,flag):

		cornerTiles = [0,2,3,5,6,8]
		allowedBlocks  = []

		if oldMove[0] in cornerTiles and oldMove[1] in cornerTiles:

			if oldMove[0] % 3 == 0 and oldMove[1] % 3 == 0:
				allowedBlocks = [0, 1, 3]

			elif oldMove[0] % 3 == 0 and oldMove[1] in [2, 5, 8]:
				allowedBlocks = [1,2,5]

			elif oldMove[0] in [2,5, 8] and oldMove[1] % 3 == 0:
				allowedBlocks  = [3,6,7]

			elif oldMove[0] in [2,5,8] and oldMove[1] in [2,5,8]:
				allowedBlocks = [5,7,8]
		else:
			if oldMove[0] % 3 == 0 and oldMove[1] in [1,4,7]:
				allowedBlocks = [1]

			elif oldMove[0] in [1,4,7] and oldMove[1] % 3 == 0:
				allowedBlocks = [3]

			elif oldMove[0] in [2,5,8] and oldMove[1] in [1,4,7]:
				allowedBlocks = [7]

			elif oldMove[0] in [1,4,7] and oldMove[1] in [2,5,8]:
				allowedBlocks = [5]

			elif oldMove[0] in [1,4,7] and oldMove[1] in [1,4,7]:
				allowedBlocks = [4]

		for i in reversed(allowedBlocks):
			if tempBlock[i] != '-':
				allowedBlocks.remove(i)

		if self.first == 0:
			self.first = 1
			cells = []
			mv = []
			ball = copy.deepcopy(allowedBlocks)
			if len(ball) == 0:
				for i in xrange(9):
					if tempBlock[i] == '-':
						ball.append(i)
			for i in ball:
				var = self.analyze(state,i,flag)
				cells.append(var)
			for i in cells:
				if i != (-1,-1):
					mv.append(i)
			for i in mv:
				if (((i[0]/3)*3) + (i[1]%3)) in cornerTiles:
					return i
			if len(mv) != 0:
				return mv[0]
			mv = []
			for i in ball:
				var = self.analyze(state,i,self.op(flag))
				cells.append(var)
			for i in cells:
				if i != (-1,-1):
					mv.append(i)
			for i in mv:
				if (((i[0]/3)*3) + (i[1]%3)) in cornerTiles:
					return i
			if len(mv) != 0:
				return mv[0]

		cells = []

		aBlockList = []
		self.scoresStored = [0]*8
		self.filter(tempBlock, flag)
		aBlockList.append(self.select(allowedBlocks, tempBlock))
		cells = self.emptyCells(state,aBlockList,tempBlock)

		return cells

	def op(self, flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	def __min_val_ab(self,state, depth, tempBlock, flag, oldMove, alpha=-(MAXX), beta=(MAXX)):
		if self.isTerminal(state, depth, tempBlock):
			return self.__eval_state(state, tempBlock, flag)
		val = (self.maxxx)
		for act in self.legalActions(state,tempBlock,oldMove,flag):
			successorState = self.generateSuccessor(state, act, flag)
			val = min(val, self.__max_val_ab(successorState,  depth - 1, tempBlock, flag, oldMove, alpha, beta))
			if val <= alpha:
				return val
			beta = min(beta, val)
		return val

	def __max_val_ab(self,state, depth, tempBlock,flag, oldMove, alpha=-(MAXX), beta=(MAXX)):
		if self.isTerminal(state, depth, tempBlock):
			return self.__eval_state(state, tempBlock, flag)
		val = -(self.maxxx)
		for act in self.legalActions(state,tempBlock,oldMove,flag):
			successorState = self.generateSuccessor(state, act, flag)
			val = max(val, self.__min_val_ab(successorState, depth, tempBlock, flag, oldMove, alpha, beta))
			if val >= beta:
				return val
			alpha = max(alpha, val)
		return val

	def isTerminal(self,state, depth, tempBlock):
		if depth==0:
			return True
		a,b =  self.terminalReached(state, tempBlock)
		return a

	def generateSuccessor(self, state, action, flag):
		brd = copy.deepcopy(state)
		brd[action[0]][action[1]] = flag
		return brd

	def __eval_state(self,state, tempBlock, flag):
		overallBoard = copy.deepcopy(state)
		innerBoard = copy.deepcopy(tempBlock)

		if self.getWinner(tempBlock) != False:
			free_cells = 0
			for i in xrange(9):
				for j in xrange(9):
					if overallBoard[i][j] == '-':
						free_cells += 1
			return self.WIN_SCORE + free_cells if self.getWinner(tempBlock) == flag else -self.WIN_SCORE - free_cells

		if self.isFull(overallBoard):
			return 0

		miniBoard = []
		for i in xrange(9):
			miniBoard.append(tempBlock[i])

		ret = self.__assess_miniB(miniBoard, flag) * self.OVERALL_BOARD_WEIGHT
		for i in xrange(9):
			if tempBlock[i] == '-':
				miniB = self.getMiniBoard(overallBoard,i)
				if '-' in miniB:
					ret += self.__assess_miniB(miniB, flag)
		return ret

	def __assess_miniB(self,miniB, flag):
		if '-' not in miniB:
			return 0
		cPlayer = 0
		cOpponent = 0
		sPlayer = flag
		sOpponent = self.op(flag)
		miniBList = copy.deepcopy(miniB)
		for seq in self.WIN_SEQ:
			filteredSeq = [miniBList[index] for index in seq if miniBList[index] != '-']
			if sPlayer in filteredSeq:
				if sOpponent in filteredSeq:
					continue
				if len(filteredSeq) > 1:
					cPlayer += self.APPROX_WIN_SCORE
				cPlayer += 1
			elif sOpponent in filteredSeq:
				if len(filteredSeq) > 1:
					cOpponent += self.APPROX_WIN_SCORE
				cOpponent += 1
		return cPlayer - cOpponent

	def getWinner(self, block):
		if block[0] == block[1] and block[1] == block[2] and block[1] != '-':
			return block[0]
		elif block[3] == block[4] and block[4] == block[5] and block[4] != '-':
			return block[3]
		elif block[6] == block[7] and block[7] == block[8] and block[7] != '-':
			return block[6]
		elif block[0] == block[3] and block[3] == block[6] and block[3] != '-':
			return block[0]
		elif block[1] == block[4] and block[4] == block[7] and block[4] != '-':
			return block[1]
		elif block[2] == block[5] and block[5] == block[8] and block[5] != '-':
			return block[2]
		elif block[0] == block[4] and block[4] == block[8] and block[4] != '-':
			return block[0]
		elif block[2] == block[4] and block[4] == block[6] and block[4] != '-':
			return block[2]
		else:
			return False

	def isFull(self,overallBoard):
		for i in xrange(9):
			if '-' in overallBoard[i]:
				return False
		return True

	def getMiniBoard(self,state,i):
		mini = []
		for x in xrange(3):
			for y in xrange(3):
				mini.append(state[i/3 + x][i%3 + y])
		return mini

	def emptyCells(self, gameb, blal,blockStat):
		cells = []
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		if cells == []:
			for i in range(9):
				for j in range(9):
					no = (i/3)*3
					no += (j/3)
					if gameb[i][j] == '-' and blockStat[no] == '-':
						cells.append((i,j))
		return cells


	def terminalReached(self,gameBoard, blockStat):

		bs = blockStat
		if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='d') or (bs[3]!='d' and bs[3]!='-' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='d' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
			# blockStat
			return True, 'W'

		elif (bs[0]!='d' and bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-') or (bs[1]!='d'and bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-') or (bs[2]!='d' and bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-'):
			# blockStat
			return True, 'W'

		elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='d') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='d'):
			# blockStat
			return True, 'W'

		else:
			smfl = 0
			for i in range(9):
				for j in range(9):
					if gameBoard[i][j] == '-' and blockStat[(i/3)*3+(j/3)] == '-':
						smfl = 1
						break
			if smfl == 1:
				return False, 'Continue'

			else:
	                        point1 = 0
	                        point2 = 0
	                        for i in blockStat:
	                            if i == 'x':
	                                point1+=1
	                            elif i=='o':
	                                point2+=1
				if point1>point2:
					return True, 'P1'
				elif point2>point1:
					return True, 'P2'
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
					    return True, 'P1'
				        elif point2>point1:
					    return True, 'P2'
	                                else:
					    return True, 'D'

	def analyze(self, gameb, index, flag):
		id1 = index/3
		id2 = index%3
		tup = []
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				tup.append(gameb[i][j])
			loc = self.free(tup,flag)
			if loc != -1:
				return (i,(id2*3)+loc)
			tup = []
		for j in range(id2*3,id2*3+3):
			for i in range(id1*3,id1*3+3):
				tup.append(gameb[i][j])
			loc = self.free(tup,flag)
			if loc != -1:
				return ((id1*3)+loc,j)
			tup = []
		for i in xrange(3):
			tup.append(gameb[id1*3+i][id2*3+i])
		loc = self.free(tup,flag)
		if loc != -1:
			return (id1*3+loc,id2*3+loc)
		tup = []
		for i in xrange(3):
			tup.append(gameb[id1*3+i][id2*3+2-i])
		loc = self.free(tup,flag)
		if loc != -1:
			return (id1*3+loc,id2*3+2-loc)
		return (-1,-1)

	def free(self, tup,flag):
		if tup[0] == tup[1] and tup[2] == '-' and tup[0] == flag:
			return 2
		elif tup[0] == tup[2] and tup[1] == '-' and tup[0] == flag:
			return 1
		elif tup[1] == tup[2] and tup[0] == '-' and tup[1] == flag:
			return 0
		else:
			return -1
