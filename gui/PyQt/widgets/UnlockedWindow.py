from PyQt6 import uic
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem, QAbstractItemView

from password_manager.manager import AutoSavingPasswordManager
from widgets.AboutAppDialog import AboutAppDialog
from widgets.CreatePassDBDialog import CreatePassDBDialog
from widgets.OpenPassDBDialog import OpenPassDBDialog
from widgets.AddPasswordDialog import AddPasswordDialog
from widgets.PasswordDialog import PasswordDialog


class UnlockedWindow(QMainWindow):
    tableWidget: QTableWidget
    actionNew: QAction
    actionOpen: QAction
    actionLock: QAction
    actionClose: QAction

    def __init__(self, welcome_screen: QMainWindow, auto_saving_manager: AutoSavingPasswordManager):
        super().__init__()
        # Load the .ui file
        uic.loadUi('ui/unlocked_window.ui', self)

        self.welcome_screen = welcome_screen
        self.auto_saving_manager = auto_saving_manager

        # Create a QAction for the button
        action = QAction("O aplikacji", self)
        action.triggered.connect(self.on_about_app_clicked)
        self.menuBar().addAction(action)

        # Connect actions in menu
        self.actionNew.triggered.connect(self.on_create_pass_db_pressed)
        self.actionOpen.triggered.connect(self.on_open_pass_db_pressed)
        self.actionLock.triggered.connect(self.on_lock_pressed)
        self.actionClose.triggered.connect(self.on_close_app_pressed)

        # About app dialog
        self.about_app_dialog = AboutAppDialog()

        # Init column view
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # Disable selection of individual cells
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Nazwa", "Ostatnio użyto"])
        for i, ratio in enumerate([0.6, 0.379]):
            self.tableWidget.setColumnWidth(i, int(self.tableWidget.width() * ratio))

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.reload_table_entries()

    def reload_table_entries(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        self.row_to_id = {}
        for i, password_id in enumerate(self.auto_saving_manager.passwords):
            password_entry = self.auto_saving_manager.passwords[password_id]
            self.row_to_id[i] = password_id
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(password_entry.name))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(password_entry.last_used_time.strftime("%d.%m.%Y")))
        self.tableWidget.clearSelection()

    def on_add_button_pressed(self):
        print("Add password entry button clicked")
        password_dialog = AddPasswordDialog()
        password_dialog.exec()

        self.auto_saving_manager.add_password_entry(password_dialog.add_update_password_entry)
        self.reload_table_entries()

    def on_remove_button_pressed(self):
        print("Remove password entry button clicked")
        selected_row_index = self.tableWidget.currentRow()
        if selected_row_index == -1:
            return
        password_entry_id = self.row_to_id[selected_row_index]
        self.auto_saving_manager.remove_password_entry(password_entry_id)
        self.reload_table_entries()

    def on_show_button_pressed(self):
        print("Show password entry button clicked")
        selected_row_index = self.tableWidget.currentRow()
        if selected_row_index == -1:
            return
        password_entry_id = self.row_to_id[selected_row_index]
        password_entry = self.auto_saving_manager.passwords[password_entry_id]
        password_dialog = PasswordDialog(state=PasswordDialog.STATES.SHOWING, password_entry=password_entry)
        password_dialog.exec()

        if password_dialog.add_update_password_entry is not None:
            self.auto_saving_manager.update_password_entry(
                id=password_entry_id,
                password_entry=password_dialog.add_update_password_entry
            )

        self.reload_table_entries()

    def on_create_pass_db_pressed(self):
        print("Create pass db button clicked")
        create_pass_db_dialog = CreatePassDBDialog()
        create_pass_db_dialog.exec()

        if create_pass_db_dialog.auto_saving_manager:
            self.welcome_screen.new_window = UnlockedWindow(
                welcome_screen=self.welcome_screen,
                auto_saving_manager=create_pass_db_dialog.auto_saving_manager
            )
            self.welcome_screen.new_window.show()

            self.close()

    def on_open_pass_db_pressed(self):
        print("Open pass db button clicked")
        open_pass_db_dialog = OpenPassDBDialog()
        open_pass_db_dialog.exec()

        if open_pass_db_dialog.auto_saving_manager:
            self.welcome_screen.new_window = UnlockedWindow(
                welcome_screen=self.welcome_screen,
                auto_saving_manager=open_pass_db_dialog.auto_saving_manager
            )
            self.welcome_screen.new_window.show()

            self.close()

    def on_lock_pressed(self):
        print("Lock button clicked")
        self.welcome_screen.show()
        self.close()

    def on_close_app_pressed(self):
        print("Exit button clicked")
        self.close()

    def on_about_app_clicked(self):
        print("About app button clicked")
        self.about_app_dialog.exec()

