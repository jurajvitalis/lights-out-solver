import constants
from PyQt5 import QtWidgets
from graph_node import Node


def dfsSolve(startNode: Node, board: QtWidgets.QWidget, render: bool) -> tuple[list, int, int]:
    marked = []
    stack = [startNode]
    expandedNodes = 0
    generatedNodes = 1

    while len(stack) > 0:

        # Vyberie posledne pridany node
        node = stack.pop()

        # Ak node este nebol expandovany, expanduj ho
        if not (node.stateLights.tolist() in marked):
            expandedNodes += 1

            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.SOLVER_MS)

            marked.append(node.stateLights.tolist())

            # Prida susedne nody do queue
            for new_node in node.getAdjacentNodes():
                generatedNodes += 1

                if not (new_node.stateLights.tolist() in marked) or not (new_node.stateLights.tolist() in stack):

                    if new_node.isSolved():

                        if render:
                            board.renderState(new_node.stateLights, new_node.stateSwitches, constants.SOLVER_MS)

                        actions = []
                        while new_node.parent is not None:
                            actions.append(new_node.action)
                            new_node = new_node.parent

                        actions.reverse()
                        return actions, expandedNodes, generatedNodes

                    stack.append(new_node)
