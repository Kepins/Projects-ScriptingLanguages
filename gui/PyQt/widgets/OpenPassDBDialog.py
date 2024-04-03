from pathlib import Path

from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.uic import loadUi

from password_manager.encryption.exceptions import DecryptionException
from password_manager.manager import ManagerFactory, AutoSavingPasswordManager
from widgets.ErrorDialog import ErrorDialog


class OpenPassDBDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/open_pass_db.ui", self)
        self.auto_saving_manager = None
        self._file_path = None

    def on_select_file_button_pressed(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz Plik", "", "Wszystkie Pliki (*)")

        if not file_path:
            print("No file selected")
            return

        self._file_path = file_path
        self.file_name_input.setText(Path(self._file_path).name)

    def on_ok_button_pressed(self):
        if not self._file_path:
            print("No file selected")
            ErrorDialog(message="Nie wybrano pliku!").exec()
            return

        master_password = self.master_password_input.text()

        if not master_password:
            ErrorDialog("Musisz podać hasło główne!").exec()
            return

        try:
            manager = ManagerFactory.from_file(self._file_path, master_password)
            self.auto_saving_manager = AutoSavingPasswordManager(manager, self._file_path, master_password)
            self.close()
        except DecryptionException:
            ErrorDialog("Nie udało się odszyfrować pliku!").exec()
        except FileNotFoundError:
            ErrorDialog("Plik nie istnieje!").exec()
