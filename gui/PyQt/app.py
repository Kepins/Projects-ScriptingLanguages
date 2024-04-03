import sys

from PyQt6.QtWidgets import QApplication

from widgets.WelcomeWindow import WelcomeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WelcomeWindow()
    main_window.show()
    sys.exit(app.exec())
