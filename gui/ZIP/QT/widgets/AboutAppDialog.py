from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi


class AboutAppDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui/about_application.ui", self)

    def on_ok_button_pressed(self):
        self.close()
