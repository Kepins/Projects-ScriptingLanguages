from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit
from PyQt6.uic import loadUi

from widgets.ErrorDialog import ErrorDialog


class ChangeMasterPasswordDialog(QDialog):
    save_button: QPushButton
    master_password_line_edit: QLineEdit
    master_password2_line_edit: QLineEdit

    def __init__(self):
        super().__init__()
        loadUi("ui/change_master_password.ui", self)

        self.new_master_password = None

    def on_save_button_pressed(self):
        print("Save button clicked")
        master_password_1 = self.master_password_line_edit.text()
        master_password_2 = self.master_password2_line_edit.text()

        if not master_password_1 or not master_password_2:
            ErrorDialog(message="Wypełnij wszystkie pola!").exec()
            return
        if master_password_1 != master_password_2:
            ErrorDialog(message="Hasła są różne!").exec()
            return

        self.new_master_password = master_password_1
        self.close()
