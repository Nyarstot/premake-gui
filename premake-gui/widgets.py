from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic import PGuiVersionString


class PGuiMainWidget(QWidget):

    def __init__(self, parent:QWidget) -> None:
        super(PGuiMainWidget, self).__init__(parent)
        self.__itnernal_init__()

    def __itnernal_init__(self) -> None:
        loadUi("./res/ui/main_widget.ui", self)

class PGuiMainWindow(QMainWindow):

    def __init__(self, version:PGuiVersionString) -> None:
        super(PGuiMainWindow, self).__init__()
        self.version_string:PGuiVersionString = version
        self.__versioned_title = f"Premake {str(self.version_string)}"

        self.__internal_init__()

    def __internal_init__(self) -> None:
        self.setWindowTitle(self.__versioned_title)
        self.setWindowIcon(QIcon("./res/icons/premake-logo.ico"))
        self.resize(1280, 720)

        self.file_menu = self.menuBar().addMenu("File")
        self.tools_menu = self.menuBar().addMenu("Tools")
        self.options_menu = self.menuBar().addMenu("Options")
        self.help_menu = self.menuBar().addMenu("Help")

        self.setCentralWidget(PGuiMainWidget(self))

