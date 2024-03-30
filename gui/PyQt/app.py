import sys

from PyQt6 import uic
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the .ui file
        uic.loadUi('ui/welcome_screen.ui', self)

        # Create a QAction for the button
        action = QAction("O aplikacji", self)
        action.triggered.connect(self.on_about_app_clicked)
        self.menuBar().addAction(action)


        # Connect actions in menu
        self.actionClose.triggered.connect(self.close)

        # About app dialog
        self.about_app_dialog = QDialog(self)
        uic.loadUi("ui/about_application.ui", self.about_app_dialog)

        # Create db dialog
        self.create_pass_db_dialog = QDialog(self)
        uic.loadUi("ui/create_pass_db.ui", self.create_pass_db_dialog)

        # Open db dialog
        self.open_pass_db_dialog = QDialog(self)
        uic.loadUi("ui/open_pass_db.ui", self.open_pass_db_dialog)


    def on_about_app_clicked(self):
        print("About app button clicked")
        self.about_app_dialog.exec()

    def on_create_pass_db_pressed(self):
        print("Create pass db button clicked")
        self.create_pass_db_dialog.exec()

    def on_open_pass_db_pressed(self):
        print("Open pass db button clicked")
        self.open_pass_db_dialog.exec()

    def on_close_app_pressed(self):
        print("Exit button clicked")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())
