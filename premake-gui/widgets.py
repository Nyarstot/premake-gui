import os
import sys
from enum import IntEnum

from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from generic import premake_executable_exists
from generic import premake_configfile_exists
from generic import PGuiVersionString
from generic import PGuiPremakeController


class PGuiMainWidget(QWidget):

    class BrowseButtonAction(IntEnum):
        SET_PREMAKE_LOCATION = 0
        SET_SOURCE_LOCATION = 1
        SET_BUILD_LOCATION = 2

    def __init__(self, parent:QWidget) -> None:
        super(PGuiMainWidget, self).__init__(parent)
        self.__itnernal_init__()
        self.__init_signals__()

    def __verify_premake_executable(self, path:str) -> bool:
        if not premake_executable_exists(path):
            QMessageBox.critical(self, "Premake not found", "Can't find premake5 executable in directory")
            return False
        return True
    
    def __verify_premake_configfile(self, path:str) -> bool:
        if not premake_configfile_exists(path):
            QMessageBox.critical(self, "premake5.lua not found", "Can't find premake5.lua file in directory")
            return False
        return True

    def __browse_button_callback(self, act:BrowseButtonAction) -> None:
        working_lineedit:QLineEdit = None
        if act == self.BrowseButtonAction.SET_PREMAKE_LOCATION:
            working_lineedit = self.premake_location_lineedit        
        elif act == self.BrowseButtonAction.SET_SOURCE_LOCATION:
            working_lineedit = self.source_location_lineedit
        elif act == self.BrowseButtonAction.SET_BUILD_LOCATION:
            working_lineedit = self.build_location_lineedit

        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        working_lineedit.setText(folder)
        print(premake_executable_exists(folder))

    def __return_lineedit_callback(self, act:BrowseButtonAction) -> None:
        if act == self.BrowseButtonAction.SET_PREMAKE_LOCATION:
            if not self.__verify_premake_executable(self.premake_location_lineedit.text()):
                return
        elif act == self.BrowseButtonAction.SET_SOURCE_LOCATION:
            if not self.__verify_premake_configfile(self.source_location_lineedit.text()):
                return
        elif act == self.BrowseButtonAction.SET_BUILD_LOCATION:
            pass

    def __itnernal_init__(self) -> None:
        loadUi("./res/ui/main_widget.ui", self)

        default_premake_path = os.path.abspath("./bin")
        self.premake_location_lineedit.setText(default_premake_path)

    def __init_signals__(self) -> None:
        self.premake_location_button.clicked.connect(lambda: self.__browse_button_callback(self.BrowseButtonAction.SET_PREMAKE_LOCATION))
        self.source_location_button.clicked.connect(lambda: self.__browse_button_callback(self.BrowseButtonAction.SET_SOURCE_LOCATION))
        self.build_location_button.clicked.connect(lambda: self.__browse_button_callback(self.BrowseButtonAction.SET_BUILD_LOCATION))
        
        self.premake_location_lineedit.returnPressed.connect(lambda: self.__return_lineedit_callback(self.BrowseButtonAction.SET_PREMAKE_LOCATION))
        self.source_location_lineedit.returnPressed.connect(lambda: self.__return_lineedit_callback(self.BrowseButtonAction.SET_SOURCE_LOCATION))
        self.build_location_lineedit.returnPressed.connect(lambda: self.__return_lineedit_callback(self.BrowseButtonAction.SET_BUILD_LOCATION))

    @property
    def premake_location(self) -> str:
        return self.premake_location_lineedit.text()
    
    @property
    def source_location(self) -> str:
        return self.source_location_lineedit.text()
    
    @property
    def build_location(self) -> str:
        return self.build_location_lineedit.text()

class PGuiMainWindow(QMainWindow):

    def __init__(self, version:PGuiVersionString) -> None:
        super(PGuiMainWindow, self).__init__()
        self.version_string:PGuiVersionString = version

        self.__main_widget = PGuiMainWidget(self)
        self.__versioned_title = f"Premake {str(self.version_string)}"
        self.__premake_controller = PGuiPremakeController()

        self.__internal_init__()

    def __internal_init__(self) -> None:
        self.setWindowTitle(self.__versioned_title)
        self.setWindowIcon(QIcon("./res/icons/premake-logo.ico"))
        self.resize(1280, 720)

        self.file_menu = self.menuBar().addMenu("File")
        self.tools_menu = self.menuBar().addMenu("Tools")
        self.options_menu = self.menuBar().addMenu("Options")
        self.help_menu = self.menuBar().addMenu("Help")

        self.setCentralWidget(self.__main_widget)

