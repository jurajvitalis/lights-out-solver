import numpy as np

TILE_SIZE = 75

patterns5 = np.zeros((5, 5, 5), int)
patterns5 = np.array([[[0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                      [[0, 0, 1, 1, 0], [0, 0, 1, 0, 0], [1, 1, 1, 0, 0], [0, 0, 1, 0, 1], [0, 0, 1, 0, 0]]])

patterns3 = np.zeros((5, 3, 2), int)
patterns3 = np.array([[[0, 1, 0], [1, 1, 1]],
                      [[1, 0, 0], [0, 1, 1]]])
