from PyQt6 import uic
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow

from password_manager.manager import AutoSavingPasswordManager
from widgets.AboutAppDialog import AboutAppDialog
from widgets.CreatePassDBDialog import CreatePassDBDialog
from widgets.OpenPassDBDialog import OpenPassDBDialog


class UnlockedWindow(QMainWindow):
    def __init__(self, welcome_screen: QMainWindow, auto_saving_manager: AutoSavingPasswordManager):
        super().__init__()
        # Load the .ui file
        uic.loadUi('ui/unlocked_window.ui', self)

        self.welcome_screen = welcome_screen
        self.auto_saving_manager = auto_saving_manager

        # Create a QAction for the button
        action = QAction("O aplikacji", self)
        action.triggered.connect(self.on_about_app_clicked)
        self.menuBar().addAction(action)

        # Connect actions in menu
        self.actionNew.triggered.connect(self.on_create_pass_db_pressed)
        self.actionOpen.triggered.connect(self.on_open_pass_db_pressed)
        self.actionLock.triggered.connect(self.on_lock_pressed)
        self.actionClose.triggered.connect(self.on_close_app_pressed)


        # About app dialog
        self.about_app_dialog = AboutAppDialog()

    def on_create_pass_db_pressed(self):
        print("Create pass db button clicked")
        create_pass_db_dialog = CreatePassDBDialog()
        create_pass_db_dialog.exec()

        if create_pass_db_dialog.auto_saving_manager:
            self.welcome_screen.new_window = UnlockedWindow(welcome_screen=self.welcome_screen, auto_saving_manager=create_pass_db_dialog.auto_saving_manager)
            self.welcome_screen.new_window.show()

            self.close()

    def on_open_pass_db_pressed(self):
        print("Open pass db button clicked")
        open_pass_db_dialog = OpenPassDBDialog()
        open_pass_db_dialog.exec()

        if open_pass_db_dialog.auto_saving_manager:
            self.welcome_screen.new_window = UnlockedWindow(welcome_screen=self.welcome_screen,
                                                            auto_saving_manager=open_pass_db_dialog.auto_saving_manager)
            self.welcome_screen.new_window.show()

            self.close()

    def on_lock_pressed(self):
        print("Lock button clicked")
        self.welcome_screen.show()
        self.close()

    def on_close_app_pressed(self):
        print("Exit button clicked")
        self.close()

    def on_about_app_clicked(self):
        print("About app button clicked")
        self.about_app_dialog.exec()

