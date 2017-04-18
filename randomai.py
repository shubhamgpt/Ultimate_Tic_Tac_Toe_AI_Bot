import sys
import random
from game import getAllEmpty
class AI:

	def __init__(self):
		pass

	def move(self,tempBoard,tempBlock,oldMove,flag):
		forCorner = [0,2,3,5,6,8]

		# allowed next blocks
		allowedBlocks  = []

		if oldMove[0] in forCorner and oldMove[1] in forCorner:
			# choose from blocks

			if oldMove[0] % 3 == 0 and oldMove[1] % 3 == 0:
				# top left corner
				allowedBlocks = [0, 1, 3]
			elif oldMove[0] % 3 == 0 and oldMove[1] in [2, 5, 8]:
				## top right corner
				allowedBlocks = [1,2,5]
			elif oldMove[0] in [2,5, 8] and oldMove[1] % 3 == 0:
				## Allowed bottom left 3 blocks
				allowedBlocks  = [3,6,7]
			elif oldMove[0] in [2,5,8] and oldMove[1] in [2,5,8]:
				### Allowed bottom right 3 blocks
				allowedBlocks = [5,7,8]
			else:
				print "Game crashed!"
				sys.exit(1)
		else:
		#### Choose only from one block (If none, free play)
			if oldMove[0] % 3 == 0 and oldMove[1] in [1,4,7]:
				## Allowed upper-center Block
				allowedBlocks = [1]

			elif oldMove[0] in [1,4,7] and oldMove[1] % 3 == 0:
				## Allowed middle-left Block
				allowedBlocks = [3]

			elif oldMove[0] in [2,5,8] and oldMove[1] in [1,4,7]:
				## Allowed lower-center Block
				allowedBlocks = [7]

			elif oldMove[0] in [1,4,7] and oldMove[1] in [2,5,8]:
				## Allowed middle-right Block
				allowedBlocks = [5]
			elif oldMove[0] in [1,4,7] and oldMove[1] in [1,4,7]:
				allowedBlocks = [4]

                for i in reversed(allowedBlocks):
                    if tempBlock[i] != '-':
                        allowedBlocks.remove(i)

	# Valid allowed empty blocks. If full, check empty cells in full board.
		cells = getAllEmpty(tempBoard,allowedBlocks,tempBlock)
		return cells[random.randrange(len(cells))]
