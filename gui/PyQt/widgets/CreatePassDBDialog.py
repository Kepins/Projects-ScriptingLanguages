from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.uic import loadUi

from password_manager.encryption.exceptions import DecryptionException
from password_manager.manager import ManagerFactory, AutoSavingPasswordManager, Manager
from widgets.ErrorDialog import ErrorDialog


class CreatePassDBDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/create_pass_db.ui", self)

        self.auto_saving_manager = None

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

        try:
            manager = Manager(new_id=1, passwords={})
            self.auto_saving_manager = AutoSavingPasswordManager(manager, file_path, master_password)
            self.close()
        except DecryptionException:
            ErrorDialog("Nie udało się odszyfrować pliku!").exec()
        except FileNotFoundError:
            ErrorDialog("Plik nie istnieje!").exec()
