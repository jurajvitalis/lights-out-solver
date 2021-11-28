import copy
import numpy as np
import constants

from PyQt5 import QtWidgets

counter = 0

class Node:
    def __init__(self, stateLights: np.ndarray, stateSwitches: np.ndarray, parent, action: tuple, cumCost: int):
        self.stateLights = stateLights
        self.stateSwitches = stateSwitches
        self.parent = parent
        self.action = action  # Action from parent to child
        self.cumCost = cumCost

    def performMove(self, row: int, col: int) -> None:
        n_rows, n_cols = self.stateLights.shape
        if row < 0 or row >= n_rows or col < 0 or col >= n_cols:
            return

        # Zapis action
        self.action = (row, col)

        # Pridaj cumCost
        self.cumCost += 1

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

    def getAdjacentNodes(self) -> list:
        if self.stateSwitches.sum() == 25:
            return []

        nodes = []
        n_rows, n_cols = self.stateLights.shape

        for r in range(n_rows):
            for c in range(n_cols):
                # if self.stateSwitches[r][c] == 1:
                #     continue

                newNode = copy.deepcopy(self)
                global counter
                counter += 1

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
    expanded_nodes = 0

    while len(stack) > 0:

        # Vyberie posledne pridany node
        node = stack.pop()

        # Ak node este nebol expandovany, expanduj ho
        if not(node.stateLights.tolist() in marked):
            expanded_nodes += 1

            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.RENDER_STATE_MS)

            marked.append(node.stateLights.tolist())

            # Prida susedne nody do queue
            for new_node in node.getAdjacentNodes():
                if not (new_node.stateLights.tolist() in marked) or not (new_node.stateLights.tolist() in stack):

                    if new_node.isSolved():

                        if render:
                            board.renderState(new_node.stateLights, new_node.stateSwitches, constants.RENDER_STATE_MS)

                        actions = []
                        while new_node.parent is not None:
                            actions.append(new_node.action)
                            new_node = new_node.parent

                        actions.reverse()
                        print(f'Pocet expandovanych uzlov: {expanded_nodes}')
                        return actions

                    stack.append(new_node)


def bfsSolveRender(startNode: Node, board: QtWidgets.QWidget, render: bool) -> list:

    marked = []
    queue = [startNode]
    expanded_nodes = 0

    while len(queue) > 0:

        # Vyberie prve pridany node
        node = queue.pop(0)
        print(f'cumCost = {node.cumCost}')

        # Ak node este nebol expandovany, expanduj ho
        if not (node.stateLights.tolist() in marked):
            expanded_nodes += 1

            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.RENDER_STATE_MS)

            # Prida node k navstivenym
            marked.append(node.stateLights.tolist())

            # Prida susedne nody do queue
            for new_node in node.getAdjacentNodes():
                if not(new_node.stateLights.tolist() in marked) or not (new_node.stateLights.tolist() in queue):

                    # Check ci tento node je final
                    if new_node.isSolved():

                        if render:
                            board.renderState(new_node.stateLights, new_node.stateSwitches, constants.RENDER_STATE_MS)

                        # Backtrack cez new_node.parent na najdenie postupnosti akcii ktore viedli k rieseniu
                        actions = []
                        while new_node.parent is not None:
                            actions.append(new_node.action)
                            new_node = new_node.parent

                        actions.reverse()
                        print(f'Pocet expandovanych uzlov: {expanded_nodes}')
                        return actions

                    queue.append(new_node)


if __name__ == '__main__':
    starttNode = Node(stateLights=constants.patterns3[1], stateSwitches=np.zeros((2, 3), int), parent=None, action=None)
    sol = dfsSolve(starttNode)

    print('Solution\n')
    print(f'moves: {sol}')
