from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi


class ErrorDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        loadUi("ui/error.ui", self)

        self.error_label.setText(message)

    def on_ok_button_pressed(self):
        self.close()
