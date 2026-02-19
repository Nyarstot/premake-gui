import sys
from PyQt5.QtWidgets import QApplication
from widgets import PGuiMainWindow
from generic import PGuiVersionString


PREMAKE_VERSION_MAJOR = 5
PREMAKE_VERSION_MINOR = 0
PREMAKE_VERSION_PATCH = 0
PREMAKE_ADDITION_STRING = "beta8"

APP_VERSION_MAJOR = 0
APP_VERSION_MINOR = 1
APP_VERSION_PATCH = 0
APP_ADDITION_STRING = "beta8"

class AppRunner(QApplication):

    def __init__(self, argv:list[str]) -> None:
        super(AppRunner, self).__init__(argv)
        
        self.premake_version = PGuiVersionString(
            PREMAKE_VERSION_MAJOR,
            PREMAKE_VERSION_MINOR,
            PREMAKE_VERSION_PATCH,
            PREMAKE_ADDITION_STRING
        )

        self.app_version = PGuiVersionString(
            APP_VERSION_MAJOR,
            APP_VERSION_MINOR,
            APP_VERSION_PATCH,
            APP_ADDITION_STRING
        )

        self.main_window = PGuiMainWindow(self.premake_version)

    def run(self) -> None:
        self.main_window.show()
        sys.exit(self.exec_())

if __name__ == "__main__":
    app = AppRunner(sys.argv)
    app.run()