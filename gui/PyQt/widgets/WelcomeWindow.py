from PyQt6 import uic
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow

from widgets.AboutAppDialog import AboutAppDialog
from widgets.CreatePassDBDialog import CreatePassDBDialog
from widgets.OpenPassDBDialog import OpenPassDBDialog


class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        uic.loadUi('ui/welcome_screen.ui', self)

        # Create a QAction for the button
        action = QAction("O aplikacji", self)
        action.triggered.connect(self.on_about_app_clicked)
        self.menuBar().addAction(action)


        # Connect actions in menu
        self.actionNew.triggered.connect(self.on_create_pass_db_pressed)
        self.actionOpen.triggered.connect(self.on_open_pass_db_pressed)
        self.actionClose.triggered.connect(self.close)

        # About app dialog
        self.about_app_dialog = AboutAppDialog()

    def on_about_app_clicked(self):
        print("About app button clicked")
        self.about_app_dialog.exec()

    def on_create_pass_db_pressed(self):
        print("Create pass db button clicked")
        create_pass_db_dialog = CreatePassDBDialog()
        create_pass_db_dialog.exec()

        print(create_pass_db_dialog.auto_saving_manager)

    def on_open_pass_db_pressed(self):
        print("Open pass db button clicked")
        open_pass_db_dialog = OpenPassDBDialog()
        open_pass_db_dialog.exec()

        print(open_pass_db_dialog.auto_saving_manager)

    def on_close_app_pressed(self):
        print("Exit button clicked")
        self.close()
