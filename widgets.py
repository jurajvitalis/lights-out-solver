import math

from PyQt5 import QtWidgets, QtGui, QtCore, sip
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import numpy as np
from timeit import default_timer as timer

import constants

clickedCounter = 0


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Lights Out')

        # Rows, cols su specific pre kazdy board, passujem do constructora
        self.bRows = 5
        self.bCols = 5
        self.bPattern = constants.patterns5[0].copy()
        self.board = Board(self.bRows, self.bCols, self.bPattern)

        self.board.won.connect(self.gameWonHandler)
        self.board.clickedSignal.connect(self.updateCount)

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
        self.patternCombox.addItem('5x5 - EASY')
        self.patternCombox.addItem('5x5 - HARD')
        self.patternCombox.addItem('2x3 - EASY')
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
        self.newGameBtn.hide()

        # Create nClicks label
        self.nClicksLabel = QtWidgets.QLabel()
        self.nClicksLabel.setFixedWidth(100)
        self.nClicksLabel.setFixedHeight(50)
        self.nClicksLabel.setText("Moves: " + str(clickedCounter))
        self.nClicksLabel.setObjectName('nClicksLabel')
        self.nClicksLabel.setAlignment(Qt.AlignCenter)

        # Timer label
        self.timerLabel = QtWidgets.QLabel(f'{0} sec')

        # Timer pre updatovanie labelu
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTimeElapsed)
        self.timer.start(constants.TICKRATE)
        self.timerStart = None

        # Create layout

        # Top layout
        self.topMenuLayout = QtWidgets.QHBoxLayout()
        self.topMenuLayout.addWidget(self.resetBtn, alignment=Qt.AlignLeft)
        self.topMenuLayout.addWidget(self.newGameBtn, alignment=Qt.AlignCenter)
        self.topMenuLayout.addWidget(self.patternCombox, alignment=Qt.AlignRight)

        # Bottom layout
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.addWidget(self.nClicksLabel, alignment=Qt.AlignLeft)
        self.bottomLayout.addWidget(self.timerLabel, alignment=Qt.AlignRight)

        # Vertical layout
        self.windowLayout = QtWidgets.QVBoxLayout()
        self.windowLayout.addLayout(self.topMenuLayout)
        self.windowLayout.addWidget(self.board, alignment=Qt.AlignCenter)
        self.windowLayout.addLayout(self.bottomLayout)

        window = QWidget()
        window.setLayout(self.windowLayout)
        self.setCentralWidget(window)

        self.timerStart = timer()

    def patternComboxHandler(self, itemID: int) -> None:
        """Zmeni board na vybrany board z combo boxu"""

        global clickedCounter
        clickedCounter = 0
        self.updateCount()

        self.resetTimer()

        # Zmaz povodny board
        self.board.setParent(None)
        sip.delete(self.board)

        # Vytvor novy board
        clickedCounter = 0
        patternID = itemID % 2
        if itemID <= 1:
            self.board = Board(5, 5, constants.patterns5[patternID])
            self.board.won.connect(self.gameWonHandler)
            self.board.clickedSignal.connect(self.updateCount)
        else:
            self.board = Board(2, 3, constants.patterns3[patternID])
            self.board.won.connect(self.gameWonHandler)
            self.board.clickedSignal.connect(self.updateCount)

            for i in range(0, 10):
                QtWidgets.QApplication.processEvents()

            self.resize(self.minimumSizeHint())

        # Pridaj novy board do layoutu
        self.windowLayout.insertWidget(1, self.board, alignment=Qt.AlignCenter)

    def resetBtnClicked(self):
        """Vymaze self.board a prida novy fresh (xddd) object"""

        global clickedCounter
        clickedCounter = 0
        self.updateCount()

        self.resetTimer()

        # Vytvor novy board
        newBoard = Board(self.board.rows, self.board.cols, self.board.pattern)

        # Signal -> Slot relation musi byt definovany pre kazdy jeden board object!
        # Treba ho teda pridat VZDY PRI RESETOVANI boardu (nie v Board lebo by sme nevedeli callovat newGameBtn)
        newBoard.won.connect(self.gameWonHandler)
        newBoard.clickedSignal.connect(self.updateCount)

        # Zmaz povodny board
        self.board.setParent(None)
        sip.delete(self.board)

        # Pridaj novy board do layoutu
        self.board = newBoard
        self.windowLayout.insertWidget(1, self.board, alignment=Qt.AlignCenter)

    def showTimeElapsed(self):
        if self.timerStart is not None:
            timerEnd = timer()
            timeElapsed = timerEnd - self.timerStart

            seconds = int(round(timeElapsed % 60, 0))
            minutes = math.floor(timeElapsed / 60)
            self.timerLabel.setText(f'{minutes}:{seconds:02d}')

    def resetTimer(self):
        self.timerStart = timer()
        self.timerLabel.setText('0. sec')
        self.timer.start()

    def updateCount(self):
        self.nClicksLabel.setText("Moves: " + str(clickedCounter))

    def gameWonHandler(self):
        self.newGameBtn.show()
        self.timer.stop()
        print('GG')

    def newGameBtnClicked(self):
        self.newGameBtn.hide()
        self.resetBtnClicked()
        self.timer.start()


class Board(QtWidgets.QWidget):
    """Reprezentuje celu hraciu plochu, aj graficku aj maticovu reprezentaciu"""

    won = QtCore.pyqtSignal()
    clickedSignal = QtCore.pyqtSignal()

    def __init__(self, rows: int, cols: int, pattern: np.ndarray):
        super().__init__()

        # nastavenie 5x5, 2x3
        self.rows = rows
        self.cols = cols
        self.pattern = pattern
        self.matrix = pattern.copy()

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setSpacing(2)
        gridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

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

        global clickedCounter
        clickedCounter = clickedCounter + 1
        self.clickedSignal.emit()

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
        # print(arr, '\n')

        sum1 = arr.sum()
        # print(sum1, '\n')

        if sum1 == 0:
            self.won.emit()
            clickedCounter = 0


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
