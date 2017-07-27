import math
import random
import cProfile

from strategy import Strategy

class StrategySet:
	def __init__(self, functions, size=100):
		assert(size>=2)
		self.functions = functions
		self.size = size
		self.strategies = []
		for _ in range(size):
			
			self.strategies.append(Strategy.generateRandomStrategy(functions))

	def nextGeneration(self, tetronimoes):
		scores = [(strategy, strategy.score(tetronimoes)) for strategy in self.strategies]
		scores.sort(reverse=True, key=lambda x: x[1])

		# keep best 25%
		self.strategies = []
		for i in range(int(self.size/4)):
			self.strategies.append(scores[i][0])

		# generate 10% new data for the gene pool
		for _ in range(int(self.size/10)):
			self.strategies.append(Strategy.generateRandomStrategy(self.functions))

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


	def iterateGenerations(self, tetronimoes, generations=20):
		for _ in range(generations):
			result = self.nextGeneration(tetronimoes)
			print(result)
