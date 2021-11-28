import copy
import numpy as np
import constants

from PyQt5 import QtWidgets


class Node:
    def __init__(self, stateLights: np.ndarray, stateSwitches: np.ndarray, parent, action: tuple):
        self.stateLights = stateLights
        self.stateSwitches = stateSwitches
        self.parent = parent
        self.action = action  # Action from parent to child

    def performMove(self, row: int, col: int) -> None:
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

    def getAdjacentNodes(self) -> list:
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


def dfsSolve(startNode: Node, board: QtWidgets.QWidget, render: bool) -> list:

    marked = []
    stack = [startNode]

    while len(stack) > 0:

        # Vyberie posledne pridany node
        node = stack.pop()

        # Ak node este nebol navstiveny, navstiv ho
        if not(node.stateSwitches.tolist() in marked):

            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.RENDER_STATE_MS)

            # Check ci tento node je final
            if node.isSolved():

                # Backtrack cez node.parent na najdenie postupnosti akcii ktore viedli k rieseniu
                actions = []
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent

                actions.reverse()
                return actions

            # Prida node k navstivenym
            marked.append(node.stateSwitches.tolist())

            # Prida susedne nody do stacku
            for new_node in node.getAdjacentNodes():
                if not(new_node.stateSwitches.tolist() in marked):
                    stack.append(new_node)


def bfsSolveRender(startNode: Node, board: QtWidgets.QWidget, render: bool) -> list:

    marked = []
    queue = [startNode]

    while len(queue) > 0:

        # Vyberie prve pridany node
        node = queue.pop(0)

        # Ak node este nebol navstiveny, navstiv ho
        if not (node.stateLights.tolist() in marked):

            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.RENDER_STATE_MS)

            # Check ci tento node je final
            if node.isSolved():

                # Backtrack cez node.parent na najdenie postupnosti akcii ktore viedli k rieseniu
                actions = []
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent

                actions.reverse()
                return actions

            # Prida node k navstivenym
            marked.append(node.stateLights.tolist())

            # Prida susedne nody do queue
            for new_node in node.getAdjacentNodes():
                if not (new_node.stateLights.tolist() in marked):
                    queue.append(new_node)


if __name__ == '__main__':
    starttNode = Node(stateLights=constants.patterns3[1], stateSwitches=np.zeros((2, 3), int), parent=None, action=None)
    sol = dfsSolve(starttNode)

    print('Solution\n')
    print(f'moves: {sol}')
