from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
import constants

import numpy as np


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lights Out')
        self.setCentralWidget(Board())


class Board(QtWidgets.QWidget):
    """Reprezentuje celu hraciu plochu, aj graficku aj maticovu reprezentaciu"""
    def __init__(self):
        super().__init__()

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setSpacing(5)

        # Pridanie squares do gridLayout
        for i in range(0, 5):
            for j in range(0, 5):
                square = Square()
                square.clicked.connect(lambda: self.squareClicked())
                gridLayout.addWidget(square, i, j)

        self.setLayout(gridLayout)

        # Matica reprezentujuca hraciu plochu
        self.matrix = []
        self.initMatrix()

    def squareClicked(self) -> None:
        """
        Click event pre policko.
        Definovany tu v Board, aby sme vedeli ziskat poziciu Square v Board layoute
        """

        # Ziskaj square a jeho poziciu v gride
        square = self.sender()
        idx = self.layout().indexOf(square)
        pos = self.layout().getItemPosition(idx)[:2]

        # Zisti ktore policka boly affectnute klikom
        squaresAffected = []

        if 0 <= pos[1] - 1 <= 4:
            squaresAffected.append(self.layout().itemAtPosition(pos[0], pos[1] - 1).widget())

        if 0 <= pos[1] + 1 <= 4:
            squaresAffected.append(self.layout().itemAtPosition(pos[0], pos[1] + 1).widget())

        if 0 <= pos[0] - 1 <= 4:
            squaresAffected.append(self.layout().itemAtPosition(pos[0] - 1, pos[1]).widget())

        if 0 <= pos[0] + 1 <= 4:
            squaresAffected.append(self.layout().itemAtPosition(pos[0] + 1, pos[1]).widget())

        squaresAffected.append(square)

        # Flipni switch pre affektnute policka
        for t in squaresAffected:
            idt = self.layout().indexOf(t)
            post = self.layout().getItemPosition(idt)[:2]

            if t.isOn:
                t.turnOff()
                self.matrix[post[0]][post[1]] = 0
            else:
                t.turnOn()
                self.matrix[post[0]][post[1]] = 1

        arr = np.array(self.matrix)
        print(arr, '\n')

    def initMatrix(self) -> None:
        """Inicializuje maticu na same 0"""
        for i in range(0, 5):
            new = []
            for j in range(0, 5):
                new.append(0)
            self.matrix.append(new)


class Square(QtWidgets.QLabel):
    """Reprezentuje jedno policko na hracej ploche"""
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.isOn = False

        self.setFixedSize(QtCore.QSize(constants.TILE_SIZE, constants.TILE_SIZE))

        pixmap = QtGui.QPixmap(constants.TILE_SIZE, constants.TILE_SIZE)
        self.setPixmap(pixmap)

        self.turnOff()

    def turnOn(self):
        self.isOn = 1
        self.drawSquare(Qt.white)

    def turnOff(self):
        self.isOn = 0
        self.drawSquare(Qt.gray)

    def drawSquare(self, color) -> None:
        """Vykresli jedno policko (stvorec)"""
        painter = QtGui.QPainter(self.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)
        painter.setBrush(QtGui.QBrush(color, Qt.SolidPattern))
        painter.drawRect(0, 0, constants.TILE_SIZE, constants.TILE_SIZE)
        painter.end()
        self.update()

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
