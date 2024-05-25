import gi

from password_manager.manager import AddUpdatePasswordEntry
from widgets.ErrorDialog import build_error_dialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def _on_add_button_pressed(button):
    dialog = button.get_toplevel()

    name = dialog.name_entry.get_text()
    username = dialog.username_entry.get_text()
    password = dialog.password_entry.get_text()

    if not name or not username or not password:
        build_error_dialog(error_message="Wypełnij wszystkie pola!").run()
        return

    dialog.add_update_password_entry = AddUpdatePasswordEntry(
        name=name, username=username, password=password
    )
    dialog.destroy()


def _on_delete_event(widget, event):
    dialog = widget.get_toplevel()
    dialog.destroy()


def build_add_password_dialog():
    handlers = {
        "on_add_button_pressed": _on_add_button_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/add_password_dialog.glade")
    builder.connect_signals(handlers)

    dialog = builder.get_object("AddPasswordDialog")
    dialog.connect("delete-event", _on_delete_event)

    dialog.add_update_password_entry = None
    dialog.name_entry = builder.get_object("name_entry")
    dialog.username_entry = builder.get_object("username_entry")
    dialog.password_entry = builder.get_object("password_entry")

    return dialog