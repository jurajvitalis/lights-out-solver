# Lights out puzzle solver

![Screenshot](/assets/readme-img.png)

A GUI application to solve 2x3 / 5x5 lights out puzzles (https://en.wikipedia.org/wiki/Lights_Out_(game)).

The solver is search-algorithm based, 4 methods in total are implemented - DFS, BFS, Greedy search, A\*. A* provides the optimal solution.

## How to use the program

1. Download the executable from releases and run it

2. Choose a puzzle to solve from the drop down menu, or create a new one by clicking on the tiles

3. Choose an algorithm used to solve the puzzle - DFS / BFS / Greedy / A*

4. To reset the puzzle to the original state, click **RESET**

To run it as a python script:

1. Build a conda environment from *environment.yml*
   
   ```bash
   conda env create --name envname --file=environment.yml
   ```

2. Run the script
   
   ```bash
   python __main__.py
   ```

## Dependencies

- Python 3.9.7
- Numpy 1.21.2
- Pyqt5 5.15.6
- All dependencies listed in *environment.yml*
