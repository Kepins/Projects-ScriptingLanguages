import sys

from PyQt6 import uic
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow

from widgets.AboutAppDialog import AboutAppDialog
from widgets.CreatePassDBDialog import CreatePassDBDialog
from widgets.OpenPassDBDialog import OpenPassDBDialog


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        uic.loadUi('ui/welcome_screen.ui', self)

        # Create a QAction for the button
        action = QAction("O aplikacji", self)
        action.triggered.connect(self.on_about_app_clicked)
        self.menuBar().addAction(action)


        # Connect actions in menu
        self.actionClose.triggered.connect(self.close)

        # About app dialog
        self.about_app_dialog = AboutAppDialog()

        # Create db dialog
        self.create_pass_db_dialog = CreatePassDBDialog()

        # Open db dialog
        self.open_pass_db_dialog = OpenPassDBDialog()


    def on_about_app_clicked(self):
        print("About app button clicked")
        self.about_app_dialog.exec()

    def on_create_pass_db_pressed(self):
        print("Create pass db button clicked")
        self.create_pass_db_dialog.exec()

    def on_open_pass_db_pressed(self):
        print("Open pass db button clicked")
        self.open_pass_db_dialog.exec()

    def on_close_app_pressed(self):
        print("Exit button clicked")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())
