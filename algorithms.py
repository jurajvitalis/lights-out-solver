import numpy as np

import constants


class Node:
    def __init__(self, stateLights: np.ndarray, stateSwitches: np.ndarray, parent, action: tuple):
        self.stateLights = stateLights
        self.stateSwitches = stateSwitches
        self.parent = parent
        self.action = action


class Stack:
    def __init__(self):
        self.buffer = []

    def add(self, node: Node) -> None:
        self.buffer.append(node)


class Puzzle:
    def __init__(self, startPattern: np.ndarray):
        self.startState = startPattern.copy()

    def isGoalState(self, stateLights: np.ndarray):

        if sum(stateLights) == 0:
            return True

    def solveDFS(self) -> list:
        pass

    def solveGreedy(self) -> list:
        pass

    def solveA(self) -> list:
        pass
