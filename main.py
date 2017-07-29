##
## Currently this game is implemented as 1010 or TenTrix, where instead of
## the tetronimoes moving down the screen, they can be placed anywhere on
## the grid.
##

import cProfile
import argparse

import csv
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

def totalEmptyTilesSurroundedByEmpty(grid):
	aloneTiles = 0
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			if grid[x][y] == 0:
				pointSum = 0
				ddx = [0, 0, 1, -1, 1, 1, -1, -1]
				ddy = [1, -1, 0, 0, 1, -1, 1, -1]
				for (dx, dy) in zip(ddx, ddy):
					if isWithinGrid(grid, x+dx, y+dy) and grid[x+dx][y+dy] != 0:
						pointSum += 1
				if pointSum == 0:
					aloneTiles += 1
	return aloneTiles

def groupsOfFour(grid):
	groups = 0
	x=y=0
	while x+1 < len(grid):
		while(y+1 < len(grid[x])):
			squareSum = 0
			ddx = [0, 0, 1, 1]
			ddy = [0, 1, 0, 1]
			for (dx, dy) in zip(ddx, ddy):
				if grid[x+dx][y+dy] == 0:
					squareSum += 1
			if squareSum == 0:
				groups += 1
			y += 2
		x += 2
	return groups

def emptyRowsAndColumns(grid):
	emptyLine = 0
	for rown in range(len(grid)):
		if sum(grid[rown]) == 0:
			emptyLine += 1

	for coln in range(len(grid[0])):
		if sum(grid[i][coln] for i in range(len(grid))) == 0:
			emptyLine += 1
	return emptyLine

def longestDiagonal(grid):
	longest = 0
	for x in range(len(grid)):
		for y in range(len(grid[x])):
			length = 0
			dx=dy=0
			while isWithinGrid(grid, x+dx, y+dy) and grid[x+dx][y+dy] == 0:
				length += 1
				dx += 1
				dy += 1
			if length > longest:
				longest = length
	return longest


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
	functions = [sumOfFullTiles, averageSurroundingEmptyTiles, largestNumberOfTransitions, totalEmptyTilesAlone, totalEmptyTilesSurroundedByEmpty, groupsOfFour, emptyRowsAndColumns, longestDiagonal]

	if args.input and os.path.isfile(args.input):
		s = StrategySet(functions, args.input)
	else:
		s = StrategySet(functions, None)

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
