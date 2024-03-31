from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.uic import loadUi

from widgets.ErrorDialog import ErrorDialog


class CreatePassDBDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/create_pass_db.ui", self)

    def on_ok_button_pressed(self):
        master_password = self.master_password_input.text()

        if not master_password:
            ErrorDialog("Musisz podać hasło główne!").exec()
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Wybierz Plik", "", "Wszystkie Pliki (*)")

        if not file_path:
            print("No file selected")
            ErrorDialog(message="Nie wybrano pliku!").exec()
            return

        print(master_password)
        print(file_path)
