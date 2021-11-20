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


def greedy(tiles: List) -> list:

    listOfTiles = [tiles]
    rows = []
    cols = []

    while isSolved == false:

        correctRow = 0  # tile s ktorou budeme hrat
        correctCol = 0
        numberOfLights = 10  # jej cislo svietiacich tiles

        # cyklus na prejdenie 2d pola s tiles
        for i in listOfTiles:
            for j in listOfTiles:

                # vykonanie zapnutia tile
                move(i, j)

                # porovnanie s predchadajucou
                if self.stateLights.sum() < numberOfLights:
                    numberOfLights = stateLights.sum()
                    # ak po nej ostane menej svietiacich, stava sa correct tile a zapiseme kde je v poli
                    correctRow = i
                    correctCol = j

                # vratenie do povodneho stavu
                move(i, j)

        # ked prejde vsetky, pozname uz correct tile a mozme s nou urobit zmenu

        move(correctRow, correctCol)

        rows.append(correctRow)
        cols.append(correctCol)
