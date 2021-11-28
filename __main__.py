from PyQt5 import QtWidgets
import sys
import widgets

if __name__ == "__main__":
    # Create application
    app = QtWidgets.QApplication(sys.argv)

    # Create main window
    window = widgets.MainWindow()
    window.show()

    # Start event loop
    app.exec()
