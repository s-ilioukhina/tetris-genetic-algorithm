# Genetic Algorithm TenTrix

This was created to dabble a bit more in genetic algorithms, and play around with what ways work best for choosing what gets passed to next generations. It is not hardcoded which scores to treat as rewards and which as penalties,  leaving it all for the strategy to decide.

This game structure is more similar to a 1010 than tetris. The tetronimoes do not descend from the top but rather can be place down anywhere on the grid. Similar optimisations apply in this version of the game. 

I used 8 fitness functions to construct a strategy's utility function:

- *sumOfFullTiles* returns the total number of empty tiles in the grid
- *averageSurroundingEmptyTiles* counts the number of tiles directly above and below each empty tile, than averages this. It is intended to encourage clustering all the empty tiles together
- *largestNumberOfTransitions* goes down each row and counts how many times the tiles transitioned between 1 and 0
- *totalEmptyTilesAlone* counts how many empty tiles were left stranded and surounded by full tiles
- *totalEmptyTilesSurroundedByEmpty* counts the number of empty tiles fully surrounded by 8 empty ones
- *groupsOfFour* counts the number of 4 full tiles grouped together
- *emptyRowsAndColumns* adds up the number of fully empty rows and columns
- *longestDiagonal* finds the number of tiles in the longest diagonal that goes from top-left to bottom-right

## Choosing the Next Generation

This part of the code can be found in strategySet.py

The next generation is filled with the data that performed best, with some new random data, and mutated data. The mutations occurs either by switching places of 2 fitness values or by averaging the full chromosome per a sample.


## Example of Game Play

Here is some output on the first round before generations of mutations occur.

[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 1, 1, 1, 0, 0]  
[0, 0, 0, 0, 0, 1, 1, 1, 1, 0]  
[0, 1, 0, 1, 1, 1, 0, 1, 1, 1]  
[0, 1, 1, 1, 1, 1, 1, 1, 1, 1]  
[1, 1, 1, 1, 1, 0, 1, 1, 1, 1]  

[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 1, 1, 1, 1, 1, 0, 0]  
[0, 0, 0, 1, 1, 1, 1, 1, 1, 0]  
[0, 1, 0, 1, 1, 1, 0, 1, 1, 1]  
[0, 1, 1, 1, 1, 1, 1, 1, 1, 1]  
[1, 1, 1, 1, 1, 0, 1, 1, 1, 1]  

[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[1, 0, 0, 1, 1, 1, 1, 1, 0, 0]  
[1, 0, 0, 1, 1, 1, 1, 1, 1, 0]  
[1, 1, 0, 1, 1, 1, 0, 1, 1, 1]  
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  
[1, 1, 1, 1, 1, 0, 1, 1, 1, 1]