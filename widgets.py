from PyQt5 import QtWidgets, QtGui, QtCore, sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import numpy as np

import constants


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lights Out')

        # Rows, cols su specific pre kazdy board, passujem do constructora
        self.bRows = 5
        self.bCols = 5
        self.bPattern = constants.patterns5[0]
        self.board = Board(self.bRows, self.bCols, self.bPattern)
        self.board.won.connect(lambda: self.newGameOption())

        # Create RESET button
        self.resetBtn = QtWidgets.QPushButton()
        self.resetBtn.setFixedWidth(100)
        self.resetBtn.setFixedHeight(50)
        self.resetBtn.setText('RESET')
        self.resetBtn.setObjectName('resetBtn')
        self.resetBtn.clicked.connect(self.resetBtnClicked)

        # Create PATTERN ComboBox
        self.patternCombox = QtWidgets.QComboBox()
        self.patternCombox.setFixedWidth(125)
        self.patternCombox.setFixedHeight(25)
        self.patternCombox.addItem('5x5 - EZ')
        self.patternCombox.addItem('5x5 - HARD')
        self.patternCombox.addItem('2x3 - EZ')
        self.patternCombox.addItem('2x3 - HARD')
        self.patternCombox.setObjectName('patternBtn')
        self.patternCombox.currentIndexChanged.connect(self.patternComboxHandler)

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
        self.menuLayout.addWidget(self.patternCombox, 0, 2)

        self.setCentralWidget(window)

    def patternComboxHandler(self, itemID: int) -> None:

        # Zmaz povodny board
        self.board.setParent(None)
        sip.delete(self.board)

        # Vytvor novy board
        patternID = itemID % 2
        if itemID <= 1:
            self.board = Board(5, 5, constants.patterns5[patternID])
        else:
            self.board = Board(2, 3, constants.patterns3[patternID])

        # Pridaj novy board do layoutu
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

    def __init__(self, rows, cols, pattern):
        super().__init__()

        # nastavenie 5x5, 2x3
        self.rows = rows
        self.cols = cols

        # Vyber default patternu
        self.curLayout = 0
        self.matrix = pattern.copy()

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setSpacing(5)

        # Pridanie squares do gridLayout

        for i in range(0, rows):
            for j in range(0, cols):
                square = Square()
                if self.matrix[i][j] == 1:
                    square.turnOn()

                square.clicked.connect(lambda: self.squareClicked())
                gridLayout.addWidget(square, i, j)

        self.setLayout(gridLayout)

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

        if 0 <= pos[1] - 1 <= self.cols - 1:
            squaresAffected.append(self.layout().itemAtPosition(pos[0], pos[1] - 1).widget())

        if 0 <= pos[1] + 1 <= self.cols - 1:
            squaresAffected.append(self.layout().itemAtPosition(pos[0], pos[1] + 1).widget())

        if 0 <= pos[0] - 1 <= self.rows - 1:
            squaresAffected.append(self.layout().itemAtPosition(pos[0] - 1, pos[1]).widget())

        if 0 <= pos[0] + 1 <= self.rows - 1:
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
