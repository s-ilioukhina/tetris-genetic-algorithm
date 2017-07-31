import random
from copy import deepcopy

GRIDSIZE = 10

class Grid:
	def __init__(self):
		self.array = [[0]*GRIDSIZE for i in range(GRIDSIZE)]

	def __getitem__(self, row):
  		return self.array[row]

	def __len__(self):
		return len(self.array)

	def isValidTetronimoPlacement(self, tetronimo, x, y):
		for (dx, dy) in tetronimo:
			if self.array[x+dx][y+dy] == 1:
				return False
		return True

	def checkRowComplete(self):
		removeRow = []
		for rown in range(len(self.array)):
			if sum(self.array[rown]) == len(self.array[rown]):
				removeRow.append(rown)

		for coln in range(len(self.array[0])):
			if sum(self.array[i][coln] for i in range(len(self.array))) == len(self.array[0]):
				for i in range(len(self.array)):
					self.array[i][coln] = 0

		# ensures row is not removed before column is checked
		for x in removeRow:
			for y in range(len(self.array[x])):
				self.array[x][y] = 0

	def placeTetronimoInGrid(self, tetronimo, x, y):
		for (dx, dy) in tetronimo:
			assert(self.array[x+dx][y+dy] == 0)
			self.array[x+dx][y+dy] += 1
		self.checkRowComplete()


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
					if grid.isValidTetronimoPlacement(tetronimo, x, y):
						for cx in range(len(grid)):
							for cy in range(len(grid[cx])):
								gridCopy[cx][cy] = grid[cx][cy]

						gridCopy.placeTetronimoInGrid(tetronimo, x, y)
						gridCopy.checkRowComplete()

						totalWeight = sum(weight * function(gridCopy) for (weight, function) in zip(self.weights, self.functions))
						if totalWeight > bestMove[1]:
							bestMove = (gridCopy, totalWeight)

			rotateTetronimo(tetronimo)
		return bestMove[0]

	def score(self, tetronimoes, debug=False, samples=20):
		def scoreGame():
			grid = Grid()

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
