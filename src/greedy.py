import constants
import heapq
from graph_node import Node
from PyQt5 import QtWidgets


def greedySolve(startNode: Node, board: QtWidgets.QWidget, render: bool) -> tuple[list, int, int]:

    prioQueue = []
    heapq.heappush(prioQueue, (startNode.hVal, startNode))
    marked = []
    expandedNodes = 0
    generatedNodes = 1

    while len(prioQueue) > 0:

        # Vyberie posledne pridany node
        node = heapq.heappop(prioQueue)[1]

        if node.isSolved():
            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.SOLVER_MS)

            actions = []
            while node.parent is not None:
                actions.append(node.action)
                node = node.parent

            actions.reverse()
            return actions, expandedNodes, generatedNodes

        # Ak node este nebol expandovany, expanduj ho
        if not(node.stateLights.tolist() in marked):

            # print(f'hVal = {node.hVal}', f'pathCost = {node.pathCost}')
            expandedNodes += 1

            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.SOLVER_MS)

            marked.append(node.stateLights.tolist())

            # Prida susedne nody do queue
            for new_node in node.getAdjacentNodes():
                generatedNodes += 1
                if not (new_node.stateLights.tolist() in marked):
                    heapq.heappush(prioQueue, (new_node.hVal, new_node))
