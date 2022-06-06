# Lights out puzzle solver

![Screenshot](/assets/readme-img.png)

A GUI application to solve custom 2x3 / 5x5 lights out puzzles (https://en.wikipedia.org/wiki/Lights_Out_(game)).

The solver is based on search algorithms, 4 methods in total are implemented - DFS, BFS, Greedy search, A\*. For optimal and the fastest solve, choose A\*.

## How to use the program

1. ```
   python __main__.py
   ```

2. Choose a puzzle to solve, or create a new one by clicking on the play tiles

3. Click DFS/BFS/Greedy/A\* **solver**

4. The solution is displayed in both the playing screen (purple dots) and the console

5. Click **RESET** to return to the unsolved puzzle

## Dependencies

Project is created with:

- Python 3.9.7
- Numpy 1.21.2
- Pyqt5 5.15.6
