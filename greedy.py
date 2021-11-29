import constants
import heapq
from graph_node import Node
from PyQt5 import QtWidgets


def greedySolve(startNode: Node, board: QtWidgets.QWidget, render: bool) -> list:

    prioQueue = []
    heapq.heappush(prioQueue, (startNode.hVal, startNode))
    marked = []
    expanded_nodes = 0

    while len(prioQueue) > 0:

        # Vyberie posledne pridany node
        node = heapq.heappop(prioQueue)[1]

        if node.isSolved():
            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.RENDER_STATE_MS)

            actions = []
            while node.parent is not None:
                actions.append(node.action)
                node = node.parent

            actions.reverse()
            print(f'Pocet expandovanych uzlov: {expanded_nodes}')
            return actions

        # Ak node este nebol expandovany, expanduj ho
        if not(node.stateLights.tolist() in marked):

            # print(f'hVal = {node.hVal}', f'pathCost = {node.pathCost}')
            expanded_nodes += 1

            if render:
                board.renderState(node.stateLights, node.stateSwitches, constants.RENDER_STATE_MS)

            marked.append(node.stateLights.tolist())

            # Prida susedne nody do queue
            for new_node in node.getAdjacentNodes():
                if not (new_node.stateLights.tolist() in marked):
                    heapq.heappush(prioQueue, (new_node.hVal, new_node))
