import numpy as np
import copy


class Node:
    def __init__(self, stateLights: np.ndarray, stateSwitches: np.ndarray, parent, action: tuple, pathCost: int):
        self.stateLights = stateLights
        self.stateSwitches = stateSwitches
        self.parent = parent
        self.action = action  # Action from parent to child
        self.pathCost = pathCost
        self.hVal = self.stateLights.sum()

    def performMove(self, row: int, col: int) -> None:
        n_rows, n_cols = self.stateLights.shape
        if row < 0 or row >= n_rows or col < 0 or col >= n_cols:
            return

        # Zapis action
        self.action = (row, col)

        # Pridaj pathCost
        self.pathCost += 1

        # Zaznamenaj zmenu v matici stateSwitches
        if self.stateSwitches[row][col] == 0:
            self.stateSwitches[row][col] = 1
        else:
            self.stateSwitches[row][col] = 0

        # Zaznamenaj zmenu v matici stateLights
        for (r, c) in ((row, col), (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
            if 0 <= r < n_rows and 0 <= c < n_cols:
                if self.stateLights[r][c]:
                    self.stateLights[r][c] = False
                else:
                    self.stateLights[r][c] = True

        # Pridaj hVal
        self.hVal = self.stateLights.sum()

    def getAdjacentNodes(self) -> list:
        if self.stateSwitches.sum() == 25:
            return []

        nodes = []
        n_rows, n_cols = self.stateLights.shape

        for r in range(n_rows):
            for c in range(n_cols):

                newNode = copy.deepcopy(self)
                newNode.parent = self
                newNode.performMove(r, c)
                nodes.append(newNode)

        return nodes

    def isSolved(self) -> bool:
        if self.stateLights.sum() == 0:
            return True

        return False

    # Arbitrary comparison definition, needed by priority queue to decide which element to pop when all are equal
    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True
