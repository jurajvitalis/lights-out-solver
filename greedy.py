import numpy as np

import constants


class Node:
    def __init__(self, stateLights: np.ndarray, stateSwitches: np.ndarray, parent, action: tuple):
        self.stateLights = stateLights
        self.stateSwitches = stateSwitches
        self.parent = parent
        self.action = action

    def isSolved(self) -> bool:
        if self.stateLights.sum() == 0:
            return True
        return False

    def move(self, row: int, col: int) -> None:
        n_rows, n_cols = self.stateLights.shape
        if row < 0 or row >= n_rows or col < 0 or col >= n_cols:
            return

        # Zapis action
        self.action = (row, col)

        # Zaznamenaj zmenu v matici stateSwitches
        self.stateSwitches[row, col] = 1

        # Zaznamenaj zmenu v matici stateLights
        for (r, c) in ((row, col), (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
            if 0 <= r < n_rows and 0 <= c < n_cols:
                if self.stateLights[r][c]:
                    self.stateLights[r][c] = False
                else:
                    self.stateLights[r][c] = True

    def greedy(self, tiles, board) -> list:

        listOfTiles = [tiles]
        finalList = []
        board = board
        explored = []

        while not self.isSolved():

            correctRow = -1  # tile s ktorou budeme hrat
            correctCol = -1
            numberOfLights = 100  # jej cislo svietiacich tiles

            x = 0
            if len(listOfTiles) == 2:
                x = 3
            else:
                x = 5

            # cyklus na prejdenie 2d pola s tiles
            for i in range(len(listOfTiles[0])):
                for j in range(x):
                    # vykonanie zapnutia tile
                    self.move(i, j)
                    # porovnanie s predchadajucou
                    if self.stateLights.sum() < numberOfLights:

                        numberOfLights = self.stateLights.sum()

                        # ak po nej ostane menej svietiacich, stava sa correct tile a zapiseme kde je v poli
                        correctRow = i
                        correctCol = j

                    # vratenie do povodneho stavu
                    self.move(i, j)

            # ked prejde vsetky, pozname uz correct tile a mozme s nou urobit zmenu

            if correctRow != -1 and correctCol != -1:

                self.move(correctRow, correctCol)
                correctTile = (correctRow, correctCol)

                board.algoRender(correctTile, 500)

                finalList.append(correctTile)
                explored.append(correctTile)

            if len(explored) == pow(len(listOfTiles[0]), x):
                explored = []

        return finalList


# if __name__ == '__main__':
#     starttNode = Node(stateLights=constants.patterns3[0], stateSwitches=np.zeros((5, 5), int), parent=None, action=None)
#     solution = starttNode.greedy(starttNode.stateLights)
#
#     print('Solution\n')
#     print(f'moves: {solution[0]}')
