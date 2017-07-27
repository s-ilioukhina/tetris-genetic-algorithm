# Genetic Algorithm Tetris

This was created to dabble a bit more in genetic algorithms, and play around with what ways work best for choosing what gets passed to next generations. It is not hardcoded which scores to treat as rewards and which as penalties,  leaving it all for the strategy to decide.

This is not the original tetris structure. The tetronimoes do not descend from the top but rather can be place down anywhere on the grid. Similar optimisations apply in this version of the game. 

It is best to keep all of the pieces together and minimise the number of gaps as tracked by the *largestNumberOfTransitions()* function. *averageSurroundingEmptyTiles()* and *totalEmptyTilesAlone()* work to minimise the number of empty tiles alone. Then of course the algorithm needs to notice when rows have been empties, which is done using *sumOfFullTiles()*.

## Choosing the Next Generation

This part of the code can be found in stratagySet.py

The next generation is filled with the data that performed best, with some new random data, and mutated data. The mutations occurs either by switching places of 2 chromosomes or by averaging the full DNA per a sample.


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