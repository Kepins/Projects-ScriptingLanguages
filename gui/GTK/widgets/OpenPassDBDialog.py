from pathlib import Path

import gi

from password_manager.encryption.exceptions import DecryptionException
from password_manager.manager import Manager, AutoSavingPasswordManager, ManagerFactory
from widgets.ErrorDialog import build_error_dialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def _on_select_file_button_pressed(button):
    dialog = button.get_toplevel()

    file_dialog = Gtk.FileChooserDialog(
        "Wybierz Plik",
        None,
        Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    response = file_dialog.run()
    file_path = file_dialog.get_filename()
    file_dialog.destroy()

    if response != Gtk.ResponseType.OK or not file_path:
        print("No file selected")
        return

    dialog.file_path = file_path
    dialog.file_name_entry.set_text(Path(dialog.file_path).name)


def _on_ok_button_pressed(button):
    dialog = button.get_toplevel()

    if not dialog.file_path:
        print("No file selected")
        build_error_dialog(error_message="Nie wybrano pliku!").run()
        return

    master_password = dialog.master_password_entry.get_text()

    if not master_password:
        build_error_dialog(error_message="Musisz podać hasło główne!").run()
        return

    try:
        manager = ManagerFactory.from_file(dialog.file_path, master_password)
        dialog.auto_saving_manager = AutoSavingPasswordManager(manager, dialog.file_path, master_password)
        dialog.destroy()
    except DecryptionException:
        build_error_dialog(error_message="Nie udało się odszyfrować pliku!").run()
    except FileNotFoundError:
        build_error_dialog(error_message="Plik nie istnieje!").run()


def _on_delete_event(widget, event):
    dialog = widget.get_toplevel()
    dialog.destroy()


def build_open_pass_db_dialog():
    handlers = {
        "on_ok_button_pressed": _on_ok_button_pressed,
        "on_select_file_button_pressed": _on_select_file_button_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/open_pass_db.glade")
    builder.connect_signals(handlers)

    dialog = builder.get_object("OpenPassDBDialog")
    dialog.connect("delete-event", _on_delete_event)

    dialog.auto_saving_manager = None
    dialog.file_path = None
    dialog.master_password_entry = builder.get_object("master_password_entry")
    dialog.file_name_entry = builder.get_object("file_name_entry")

    return dialog