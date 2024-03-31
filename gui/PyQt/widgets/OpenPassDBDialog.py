from pathlib import Path

from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.uic import loadUi

from widgets.ErrorDialog import ErrorDialog


class OpenPassDBDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/open_pass_db.ui", self)

        self.file_path = None

    def on_select_file_button_pressed(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Wybierz Plik", "", "Wszystkie Pliki (*)")

        if not file_path:
            print("No file selected")
            return

        self.file_path = file_path
        self.file_name_input.setText(Path(self.file_path).name)

    def on_ok_button_pressed(self):
        if not self.file_path:
            print("No file selected")
            ErrorDialog(message="Nie wybrano pliku!").exec()
            return

        master_password = self.master_password_input.text()

        if not master_password:
            ErrorDialog("Musisz podać hasło główne!").exec()
            return

        print(master_password)
        print(self.file_path)
