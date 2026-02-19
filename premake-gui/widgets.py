from enum import IntEnum

from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic import PGuiVersionString


class PGuiMainWidget(QWidget):

    class BrowseButtonAction(IntEnum):
        SET_PREMAKE_LOCATION = 0
        SET_SOURCE_LOCATION = 1
        SET_BUILD_LOCATION = 2

    def __init__(self, parent:QWidget) -> None:
        super(PGuiMainWidget, self).__init__(parent)
        self.__itnernal_init__()
        self.__init_signals__()

    def __browse_folder_callback(self, act:BrowseButtonAction) -> None:
        working_lineedit:QLineEdit = None
        if act == self.BrowseButtonAction.SET_PREMAKE_LOCATION:
            working_lineedit = self.premake_location_lineedit
        elif act == self.BrowseButtonAction.SET_SOURCE_LOCATION:
            working_lineedit = self.source_location_lineedit
        elif act == self.BrowseButtonAction.SET_BUILD_LOCATION:
            working_lineedit = self.build_location_lineedit

        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        working_lineedit.setText(folder)

    def __itnernal_init__(self) -> None:
        loadUi("./res/ui/main_widget.ui", self)

    def __init_signals__(self) -> None:
        self.premake_location_button.clicked.connect(lambda: self.__browse_folder_callback(self.BrowseButtonAction.SET_PREMAKE_LOCATION))
        self.source_location_button.clicked.connect(lambda: self.__browse_folder_callback(self.BrowseButtonAction.SET_SOURCE_LOCATION))
        self.build_location_button.clicked.connect(lambda: self.__browse_folder_callback(self.BrowseButtonAction.SET_BUILD_LOCATION))

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

