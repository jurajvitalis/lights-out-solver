from PyQt5 import QtWidgets, QtGui, QtCore, sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import constants

import numpy as np

# nastavenie 5x5, 2x3
x = 5
y = 5

already = 0


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lights Out')

        self.board = Board()

        self.board.won.connect(lambda: self.newGameOption())

        # Create RESET button
        self.resetBtn = QtWidgets.QPushButton()
        self.resetBtn.setFixedWidth(100)
        self.resetBtn.setFixedHeight(50)
        self.resetBtn.setText('RESET')
        self.resetBtn.setObjectName('resetBtn')
        self.resetBtn.clicked.connect(self.resetBtnClicked)

        # Create LAYOUT button
        self.layoutBtn = QtWidgets.QPushButton()
        self.layoutBtn.setFixedWidth(100)
        self.layoutBtn.setFixedHeight(50)
        self.layoutBtn.setText('LAYOUT')
        self.layoutBtn.setObjectName('layoutBtn')
        self.layoutBtn.clicked.connect(self.board.layoutBtnClicked)
        self.layoutBtn.clicked.connect(self.clicked)

        # Create NEWGAME button
        self.newGameBtn = QtWidgets.QPushButton()
        self.newGameBtn.setFixedWidth(100)
        self.newGameBtn.setFixedHeight(50)
        self.newGameBtn.setText('NEW GAME')
        self.newGameBtn.setObjectName('newGameBtn')
        self.newGameBtn.clicked.connect(self.newGameBtnClicked)

        window = QWidget()
        self.menuLayout = QtWidgets.QGridLayout(window)

        self.menuLayout.addWidget(self.board, 1, 0, 1, 2)
        self.menuLayout.addWidget(self.resetBtn, 0, 0)
        self.menuLayout.addWidget(self.layoutBtn, 0, 2)

        self.setCentralWidget(window)

    def clicked(self):
        """self.menuLayout.removeWidget(self.board)
        sip.delete(self.board)
        self.board = None"""
        self.board.setParent(None)
        self.board = Board()
        self.menuLayout.addWidget(self.board, 1, 0, 1, 2)

    def newGameOption(self):
        print("new game")
        self.menuLayout.addWidget(self.newGameBtn, 0, 1)

    def newGameBtnClicked(self):
        print("new game")
        self.newGameBtn.setParent(None)
        self.resetBtnClicked()

    def resetBtnClicked(self):
        print("reset game")
        self.board.resetBtnClicked()


class Board(QtWidgets.QWidget):
    """Reprezentuje celu hraciu plochu, aj graficku aj maticovu reprezentaciu"""

    won = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()


        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setSpacing(5)

        # Pridanie squares do gridLayout
        for i in range(0, x):
            for j in range(0, y):
                square = Square()
                square.clicked.connect(lambda: self.squareClicked())
                gridLayout.addWidget(square, i, j)

        self.setLayout(gridLayout)

        # Matica reprezentujuca hraciu plochu
        self.matrix = []
        self.initMatrix()

    def squareClicked(self) -> None:
        """
        Click event handler pre square.
        Definovany tu v Board, aby sme vedeli ziskat poziciu square v board grid layoute.
        """

        # Ziskaj square a jeho poziciu v gride
        square = self.sender()
        idx = self.layout().indexOf(square)
        pos = self.layout().getItemPosition(idx)[:2]

        # Zisti ktore policka boly affectnute klikom
        squaresAffected = []

        if 0 <= pos[1] - 1 <= y - 1:
            squaresAffected.append(self.layout().itemAtPosition(pos[0], pos[1] - 1).widget())

        if 0 <= pos[1] + 1 <= y - 1:
            squaresAffected.append(self.layout().itemAtPosition(pos[0], pos[1] + 1).widget())

        if 0 <= pos[0] - 1 <= x - 1:
            squaresAffected.append(self.layout().itemAtPosition(pos[0] - 1, pos[1]).widget())

        if 0 <= pos[0] + 1 <= x - 1:
            squaresAffected.append(self.layout().itemAtPosition(pos[0] + 1, pos[1]).widget())

        squaresAffected.append(square)

        # Flipni switch pre affektnute policka (Zapni/zhasni svetlo)
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

        sum1 = arr.sum()
        print(sum1, '\n')

        if sum1 == 0:
            self.won.emit()
            print("GAME WON")

    def initMatrix(self) -> None:

        for i in range(0, x):
            new = []
            for j in range(0, y):
                new.append(0)
            self.matrix.append(new)

    def layoutBtnClicked(self) -> None:

        global x
        global y

        if x == 5:
            x = 2
            y = 3
        else:
            x = 5
            y = 5
        print(x)
        print(y)

    def resetBtnClicked(self):

        print("hello")


class Square(QtWidgets.QLabel):
    """Reprezentuje jeden square na hracej ploche"""

    # Definicia signalu, ktory sa vysle pri kliknuti na policko
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.isOn = False

        self.setFixedSize(QtCore.QSize(constants.TILE_SIZE, constants.TILE_SIZE))

        pixmap = QtGui.QPixmap(constants.TILE_SIZE, constants.TILE_SIZE)
        self.setPixmap(pixmap)

        self.turnOff()

    def turnOn(self) -> None:
        self.isOn = 1
        self.drawSquare(Qt.white)

    def turnOff(self) -> None:
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
