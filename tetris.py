import math
import random
import cProfile
from copy import deepcopy

GRIDSIZE = 10

iBlock = [[0,0], [0,1], [0,2], [0,3]]
tBlock = [[0,0], [0,1], [1,0], [-1,0]]
jBlock = [[0,0], [-1,0], [0,1], [0,2]]
lBlock = [[0,0], [0,1], [0,2], [-1,2]]
oBlock = [[0,0], [0,1], [1,0], [1,1]]
sBlock = [[0,0], [0,1], [1,0], [1,-1]]
zBlock = [[0,0], [0,1], [1,1], [1,2]]
tetronimoes = [iBlock, tBlock, jBlock, lBlock, oBlock, sBlock, zBlock]

def isWithinGrid(grid, x, y):
	if x >= len(grid) or x < 0 or y >= len(grid[x]) or y < 0:
		return False
	return True

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

def sumOfFullTiles(grid):
	return sum(sum(row) for row in grid)

def numSurroundingEmptyTiles(grid):
	listSum = []
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			if grid[x][y] == 0:
				pointSum = 0
				ddx = [0, 0, 1, -1]
				ddy = [1, -1, 0, 0]
				for (dx, dy) in zip(ddx, ddy):
					if isWithinGrid(grid, x+dx, y+dy) and grid[x+dx][y+dy] == 0:
						pointSum += 1
				listSum.append(pointSum)

	totalSum = sum(listSum)
	return totalSum / len(listSum)


class Strategy:
	def __init__(self, functions, weights):
		assert(len(functions) == len(weights))
		self.functions = functions
		self.weights = weights

	def __repr__(self):
		return "Strategy({0})".format(",".join(map(str, self.weights)))

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

	def score(self, samples=20):
		def scoreGame():
			grid = [[0]*GRIDSIZE for i in range(GRIDSIZE)]
			score = 0
			while grid:
				tetronimo = random.choice(tetronimoes)
				grid = self.chooseMove(grid, tetronimo)
				score += 1
				#print(grid)
			return score
		return sum(scoreGame() for _ in range(samples))/samples

def generateRandomStrategy(functions):
		weights = [random.random()-0.5 for f in functions]
		weightnorm = pow(sum(w**2 for w in weights), 0.5)
		weights = [w/weightnorm for w in weights]
		return Strategy(functions, weights)


class StrategySet:
	def __init__(self, functions, size=100):
		assert(size>=2)
		self.functions = functions
		self.size = size
		self.strategies = []
		for _ in range(size):
			
			self.strategies.append(generateRandomStrategy(functions))

	def nextGeneration(self):
		scores = [(strategy, strategy.score()) for strategy in self.strategies]
		scores.sort(reverse=True, key=lambda x: x[1])

		# keep best 25%
		self.strategies = []
		for i in range(int(self.size/4)):
			self.strategies.append(scores[i][0])

		# generate 10% new data for the gene pool
		for _ in range(int(self.size/10)):
			self.strategies.append(generateRandomStrategy(self.functions))

		# for 10% of the data, randomly select 20% of the data, swap a weight in best 2
		for _ in range(int(self.size/10)):
			subset = random.sample(scores, int(self.size/5))
			subset.sort(reverse=True, key=lambda x: x[1])

			index = random.sample([i for i in range(len(subset[0][0].weights))], 2)

			subset[0][0].weights[index[0]], subset[0][0].weights[index[1]] = subset[0][0].weights[index[1]], subset[0][0].weights[index[0]]
			self.strategies.append(Strategy(self.functions, subset[0][0].weights))

		# fill the rest of the strategies with evolved data
		# randomly select 20% of the data, average the best 2
		while len(self.strategies) < self.size:
			subset = []
			if self.size >= 10:
				subset = random.sample(scores, int(self.size/5))
			else:
				subset = random.sample(scores, 2)
			subset.sort(reverse=True, key=lambda x: x[1])

			weights = [subset[0][0].weights[f]+subset[1][0].weights[f] for f in range(len(self.functions))]
			weightnorm = pow(sum(w**2 for w in weights), 0.5)
			weights = [w/weightnorm for w in weights]
			self.strategies.append(Strategy(self.functions, weights))

		#replace repeating stratagies with random weights
		self.strategies.sort(reverse=True, key=lambda x: x.weights[0])
		for i in range(self.size):
			if i != 0 and self.strategies[i-1].weights == self.strategies[i]:
				self.strategies[i-1] = generateRandomStrategy(self.functions)

		return scores[0], sum(score for (_, score) in scores)/len(scores)


	def iterateGenerations(self, generations=20):
		for _ in range(generations):
			result = self.nextGeneration()
			print(result)


def main():
	s = StrategySet([sumOfFullTiles, numSurroundingEmptyTiles])
	s.iterateGenerations()

if __name__ == '__main__':
	main()
