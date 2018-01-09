import unittest

from main import *

grid = [[0]*5 for i in range(5)]
grid[1][1] = grid[2][1] = grid[3][0] = grid[4][0] = grid[4][1] = grid[3][2] = grid[3][3] = grid[4][4] = 1

class TestFunctions(unittest.TestCase):

    def test_sum_of_full_tiles(self):
        self.assertEqual(8, sumOfFullTiles(grid))

    def test_average_surrounding_empty_tiles(self):
        self.assertEqual(2.1176470588235294, averageSurroundingEmptyTiles(grid))

    def test_largest_number_of_transitions(self):
        self.assertEqual(3, largestNumberOfTransitions(grid))

    def test_total_empty_tiles_alone(self):
        self.assertEqual(1, totalEmptyTilesAlone(grid))

    def test_total_empty_tiles_surrounded_by_empty(self):
        self.assertEqual(4, totalEmptyTilesSurroundedByEmpty(grid))

    def test_groups_of_four(self):
        self.assertEqual(0, groupsOfFour(grid))

    def test_empty_rows_and_columns(self):
        self.assertEqual(1, emptyRowsAndColumns(grid))

    def test_longest_diagonal(self):
        self.assertEqual(4, longestDiagonal(grid))


if __name__ == '__main__':
    unittest.main()
