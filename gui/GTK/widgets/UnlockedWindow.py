import gi

from password_manager.manager import AutoSavingPasswordManager
from widgets.AboutAppDialog import build_about_app_dialog
from widgets.AddPasswordDialog import build_add_password_dialog
from widgets.CreatePassDBDialog import build_create_pass_db_dialog
from widgets.OpenPassDBDialog import build_open_pass_db_dialog
from widgets.PasswordDialog import build_password_dialog, STATES

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def _on_add_button_pressed(button):
    print("Add password entry button clicked")
    window = button.get_toplevel()

    password_dialog = build_add_password_dialog()
    password_dialog.run()

    if password_dialog.add_update_password_entry is not None:
        window.auto_saving_manager.add_password_entry(password_dialog.add_update_password_entry)

    reload_table_entries(window)


def _on_remove_button_pressed(button):
    print("Remove password entry button clicked")
    window = button.get_toplevel()
    tree_view = window.tree_view

    selection = tree_view.get_selection()
    model, treeiter = selection.get_selected()
    if treeiter is not None:
        # Get the path of the selected row
        path = model.get_path(treeiter)
        # Get the row number from the path
        row_number = path.get_indices()[0]

        password_entry_id = window.row_to_id[row_number]

        window.auto_saving_manager.remove_password_entry(id=password_entry_id)

    reload_table_entries(window)


def _on_show_button_pressed(button):
    print("Show password entry button clicked")

    window = button.get_toplevel()
    tree_view = window.tree_view

    selection = tree_view.get_selection()
    model, treeiter = selection.get_selected()
    if treeiter is not None:
        # Get the path of the selected row
        path = model.get_path(treeiter)
        # Get the row number from the path
        row_number = path.get_indices()[0]

        password_entry_id = window.row_to_id[row_number]
        password_dialog = build_password_dialog(password_entry=window.auto_saving_manager.passwords[password_entry_id], state=STATES.SHOWING)
        password_dialog.run()

        if password_dialog.add_update_password_entry is not None:
            window.auto_saving_manager.update_password_entry(id=password_entry_id, password_entry=password_dialog.add_update_password_entry)

    reload_table_entries(window)


def _on_about_app_pressed(widget):
    print("About app button clicked")

    about_dialog = build_about_app_dialog()
    about_dialog.run()


def _on_create_pass_db_pressed(widget):
    print("Create pass db button clicked")
    dialog = build_create_pass_db_dialog()
    dialog.run()

    if not dialog.auto_saving_manager:
        return

    win = build_unlocked_window(dialog.auto_saving_manager)
    win.show_all()
    widget.get_toplevel().destroy()


def _on_open_pass_db_pressed(widget):
    print("Open pass db button clicked")
    dialog = build_open_pass_db_dialog()
    dialog.run()

    if not dialog.auto_saving_manager:
        return

    win = build_unlocked_window(dialog.auto_saving_manager)
    win.show_all()
    widget.get_toplevel().destroy()


def _on_save_as_pressed(widget):
    print("Save as button clicked")


def _on_change_master_password_pressed(widget):
    print("Change master password button clicked")


def _on_lock_pressed(widget):
    print("Lock button clicked")
    from widgets.WelcomeWindow import build_welcome_window
    win = build_welcome_window()
    win.show_all()
    widget.get_toplevel().destroy()


def _on_close_app_pressed(widget):
    print("Exit button clicked")
    Gtk.main_quit()


def reload_table_entries(window):
    # Clear existing data in the tree view
    software_liststore = window.tree_view.get_model()
    software_liststore.clear()

    # Populate data list with new entries
    window.row_to_id = {}
    data_list = []
    for i, password_id in enumerate(window.auto_saving_manager.passwords):
        password_entry = window.auto_saving_manager.passwords[password_id]
        data_list.append((password_entry.name, password_entry.last_used_time.strftime("%d.%m.%Y")))
        window.row_to_id[i] = password_id

    # Append new data to the tree view
    for software_ref in data_list:
        software_liststore.append(list(software_ref))

    # If columns already exist, remove them before re-adding
    for column in window.tree_view.get_columns():
        window.tree_view.remove_column(column)

    # Add new columns to the tree view
    for i, column_title in enumerate(["Nazwa", "Ostatnio użyto"]):
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(column_title, renderer, text=i)
        window.tree_view.append_column(column)


def build_unlocked_window(auto_saving_manager: AutoSavingPasswordManager):
    handlers = {
        "on_add_button_pressed": _on_add_button_pressed,
        "on_remove_button_pressed": _on_remove_button_pressed,
        "on_show_button_pressed": _on_show_button_pressed,
        "on_about_app_pressed": _on_about_app_pressed,
        "on_create_pass_db_pressed": _on_create_pass_db_pressed,
        "on_open_pass_db_pressed": _on_open_pass_db_pressed,
        "on_save_as_pressed": _on_save_as_pressed,
        "on_change_master_password_pressed": _on_change_master_password_pressed,
        "on_lock_pressed": _on_lock_pressed,
        "on_close_app_pressed": _on_close_app_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/unlocked_window.glade")
    builder.connect_signals(handlers)

    window = builder.get_object("UnlockedWindow")
    window.auto_saving_manager = auto_saving_manager
    window.tree_view = builder.get_object("tree_view")

    reload_table_entries(window)
    return window
