from enum import Enum

from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit
from PyQt6.uic import loadUi

from password_manager.manager import AddUpdatePasswordEntry, PasswordEntry
from widgets.ErrorDialog import ErrorDialog


class PasswordDialog(QDialog):
    class STATES(Enum):
        SHOWING = 0
        EDITING = 1

    name_line_edit: QLineEdit
    username_line_edit: QLineEdit
    password_line_edit: QLineEdit
    edit_button: QPushButton
    save_button: QPushButton
    cancel_button: QPushButton

    def __init__(self, state: STATES, password_entry: PasswordEntry):
        super().__init__()
        loadUi("ui/password_dialog.ui", self)

        self.state = state
        self.password_entry = password_entry
        self.add_update_password_entry = None

        self.name_line_edit.setText(password_entry.name)
        self.username_line_edit.setText(password_entry.username)
        self.password_line_edit.setText(password_entry.password)

        self.change_state(state)

    def change_state(self, state: STATES):
        if state == self.STATES.SHOWING:
            self.setWindowTitle("Wyświetl")
            self.name_line_edit.setReadOnly(True)
            self.username_line_edit.setReadOnly(True)
            self.password_line_edit.setReadOnly(True)
            self.cancel_button.hide()
            self.save_button.hide()
            self.edit_button.show()
        if state == self.STATES.EDITING:
            self.setWindowTitle("Edytuj")
            self.name_line_edit.setReadOnly(False)
            self.username_line_edit.setReadOnly(False)
            self.password_line_edit.setReadOnly(False)
            self.cancel_button.show()
            self.save_button.show()
            self.edit_button.hide()

    def on_edit_button_pressed(self):
        print("Edit button clicked")
        self.change_state(state=self.STATES.EDITING)

    def on_save_button_pressed(self):
        print("Save button clicked")
        name = self.name_line_edit.text()
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()

        if not name or not username or not password:
            ErrorDialog(message="Wypełnij wszystkie pola!").exec()
            return
        self.change_state(state=self.STATES.SHOWING)
        self.add_update_password_entry = AddUpdatePasswordEntry(name=name, username=username, password=password)

    def on_cancel_button_pressed(self):
        print("Cancel button clicked")
        self.change_state(state=self.STATES.SHOWING)
        self.name_line_edit.setText(self.password_entry.name)
        self.username_line_edit.setText(self.password_entry.username)
        self.password_line_edit.setText(self.password_entry.password)
