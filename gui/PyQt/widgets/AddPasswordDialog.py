from enum import Enum

from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.uic import loadUi

from password_manager.manager import AddUpdatePasswordEntry
from widgets.ErrorDialog import ErrorDialog


class AddPasswordDialog(QDialog):
    pushButton: QPushButton

    def __init__(self):
        super().__init__()
        loadUi("ui/add_password_dialog.ui", self)

        self.addUpdatePasswordEntry = None

    def on_add_button_pressed(self):
        print("Add button clicked")
        name = self.name_line_edit.text()
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        if not name or not username or not password:
            ErrorDialog(message="Wypełnij wszystkie pola!").exec()
            return

        self.addUpdatePasswordEntry = AddUpdatePasswordEntry(name=name, username=username, password=password)
        self.close()

