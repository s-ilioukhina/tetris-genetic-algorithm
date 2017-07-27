import random
import cProfile
from copy import deepcopy

GRIDSIZE = 10

def isValidTetronimoPlacement(grid, tetronimo, x, y):
	for (dx, dy) in tetronimo:
		if grid[x+dx][y+dy] == 1:
			return False
	return True

def placeTetronimoInGrid(grid, tetronimo, x, y):
	for (dx, dy) in tetronimo:
		assert(grid[x+dx][y+dy] == 0)
		grid[x+dx][y+dy] += 1
	checkRowComplete(grid)

def checkRowComplete(grid):
	removeRow = []
	for rown in range(len(grid)):
		if sum(grid[rown]) == len(grid[rown]):
			removeRow.append(rown)

	for coln in range(len(grid[0])):
		if sum(grid[i][coln] for i in range(len(grid))) == len(grid[0]):
			for i in range(len(grid)):
				grid[i][coln] = 0

	# ensures row is not removed before column is checked
	for x in removeRow:
		for y in range(len(grid[x])):
			grid[x][y] = 0


class Strategy:
	def __init__(self, functions, weights):
		assert(len(functions) == len(weights))
		self.functions = functions
		self.weights = weights

	def __repr__(self):
		return "{0}".format(",".join(map(str, self.weights)))

	def chooseMove(self, grid, tetronimo):
		bestMove = (None, -10e10)

		def rotateTetronimo(tetronimo):
			for i in range(len(tetronimo)):
				tetronimo[i][0], tetronimo[i][1] = tetronimo[i][1], -tetronimo[i][0]

		def tetronimoDimentions(tetronimo):
			minX = minY = maxX = maxY = 0
			for (dx, dy) in tetronimo:
				minX = dx if dx < minX else minX
				minY = dy if dy < minY else minY
				maxX = dx if dx > maxX else maxX
				maxY = dy if dy > maxY else maxY
			return minX, minY, maxX, maxY

		gridCopy = deepcopy(grid)
		for rotation in range(4):
			minX, minY, maxX, maxY = tetronimoDimentions(tetronimo)
			for x in range(-minX, len(grid) - maxX):
				for y in range(-minY, len(grid[x]) - maxY):
					if isValidTetronimoPlacement(grid, tetronimo, x, y):
						for cx in range(len(grid)):
							for cy in range(len(grid[cx])):
								gridCopy[cx][cy] = grid[cx][cy]

						placeTetronimoInGrid(gridCopy, tetronimo, x, y)
						checkRowComplete(gridCopy)

						totalWeight = sum(weight * function(gridCopy) for (weight, function) in zip(self.weights, self.functions))
						if totalWeight > bestMove[1]:
							bestMove = (gridCopy, totalWeight)

			rotateTetronimo(tetronimo)
		return bestMove[0]

	def score(self, tetronimoes, debug=False, samples=20):
		def scoreGame():
			grid = [[0]*GRIDSIZE for i in range(GRIDSIZE)]

			score = 0
			while grid:
				tetronimo = random.choice(tetronimoes)
				grid = self.chooseMove(grid, tetronimo)
				score += 1

				if debug and grid:
					for x in range(len(grid)):
						print(grid[x])
					print('')
			return score
		return sum(scoreGame() for _ in range(samples))/samples

	def generateRandomStrategy(functions):
		weights = [random.random()-0.5 for f in functions]
		weightnorm = pow(sum(w**2 for w in weights), 0.5)
		weights = [w/weightnorm for w in weights]
		return Strategy(functions, weights)
