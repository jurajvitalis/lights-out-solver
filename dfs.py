import copy
import numpy as np
import constants


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


def dfsSolve(startNode: Node) -> tuple:

    explored = []
    stack = [startNode]

    while len(stack) > 0:

        node = stack.pop()

        # Expanduj node
        #   Pridaj do explored
        #   Pozri sa na vsetky childs
        #       Checkni win condition
        #       Pridaj do stacku
        if not(node in explored):
            explored.append(node)

            for new_node in node.getAdjacentNodes():

                # Nasiel si riesenie?
                if new_node.isSolved():
                    actions = []
                    states = []

                    # Backtrack cez vsetkych rodicov, loguj action a state
                    while new_node.parent is not None:
                        actions.append(new_node.action)
                        states.append(new_node.stateSwitches)
                        new_node = new_node.parent

                    # Uprava vysledku
                    actions.reverse()
                    states.reverse()
                    return actions, states

                stack.append(new_node)


if __name__ == '__main__':
    starttNode = Node(stateLights=constants.patterns5[0], stateSwitches=np.zeros((5, 5), int), parent=None, action=None)
    sol = dfsSolve(starttNode)

    print('Solution\n')
    print(f'moves: {sol[0]}')
    print(f'flipped: \n{sol[1]}')
