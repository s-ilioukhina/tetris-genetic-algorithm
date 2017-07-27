import cProfile
import sys
import argparse

import csv
import os
import os.path

from time import gmtime, strftime

from strategySet import StrategySet

def isWithinGrid(grid, x, y):
	if x >= len(grid) or x < 0 or y >= len(grid[x]) or y < 0:
		return False
	return True

def sumOfFullTiles(grid):
	return sum(sum(row) for row in grid)

def averageSurroundingEmptyTiles(grid):
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

def largestNumberOfTransitions(grid):
	maxTransitions = 0
	for x in range(len(grid)):
		numTransitions = 0
		for y in range(len(grid[x]) - 1):
			if grid[x][y] != grid[x][y+1]:
				numTransitions += 1

		if numTransitions > maxTransitions:
			maxTransitions = numTransitions
	return maxTransitions

def totalEmptyTilesAlone(grid):
	aloneTiles = 0
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			if grid[x][y] == 0:
				pointSum = 0
				ddx = [0, 0, 1, -1]
				ddy = [1, -1, 0, 0]
				for (dx, dy) in zip(ddx, ddy):
					if isWithinGrid(grid, x+dx, y+dy) and grid[x+dx][y+dy] == 0:
						pointSum += 1
				if pointSum == 0:
					aloneTiles += 1
	return aloneTiles


def main():
	iBlock = [[0,0], [0,1], [0,2], [0,3]]
	tBlock = [[0,0], [0,1], [1,0], [-1,0]]
	jBlock = [[0,0], [-1,0], [0,1], [0,2]]
	lBlock = [[0,0], [0,1], [0,2], [-1,2]]
	oBlock = [[0,0], [0,1], [1,0], [1,1]]
	sBlock = [[0,0], [0,1], [1,0], [1,-1]]
	zBlock = [[0,0], [0,1], [1,1], [1,2]]
	tetronimoes = [iBlock, tBlock, jBlock, lBlock, oBlock, sBlock, zBlock]

	parser = argparse.ArgumentParser(description='create an AI that plays tetris.')

	parser.add_argument(
		"-o",
		"--output_dir",
		default="..",
		help="folder where to store the weights of the final generation")
	parser.add_argument(
		"-i",
		"--input",
		help="optional file containing the weights of the starting generation")

	args = parser.parse_args()

	if args.input and os.path.isfile(args.input):
		s = StrategySet([sumOfFullTiles, averageSurroundingEmptyTiles, largestNumberOfTransitions, totalEmptyTilesAlone], args.input)
	else:
		s = StrategySet([sumOfFullTiles, averageSurroundingEmptyTiles, largestNumberOfTransitions, totalEmptyTilesAlone], None)

	finalGeneration = s.iterateGenerations(tetronimoes)

	filename = 'tetris_' + strftime("%Y_%m_%d_%H_%M", gmtime()) + ".csv"
	outputFile = os.path.join(args.output_dir, filename)

	print("printing to " + outputFile)
	with open (outputFile, 'w', newline='') as outputFile:
		writer = csv.writer(outputFile)
		for strategy in finalGeneration[0]:
			writer.writerow(strategy[0].weights)

if __name__ == '__main__':
	main()
