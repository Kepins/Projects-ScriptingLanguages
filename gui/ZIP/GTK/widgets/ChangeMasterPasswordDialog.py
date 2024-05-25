import gi

from widgets.ErrorDialog import build_error_dialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def _on_ok_button_pressed(button):
    dialog = button.get_toplevel()

    master_password = dialog.master_password_entry.get_text()
    master_password2 = dialog.master_password2_entry.get_text()

    if not master_password or not master_password2:
        build_error_dialog(error_message="Wypełnij wszystkie pola!").run()
        return

    if master_password != master_password2:
        build_error_dialog(error_message="Hasła są różne!").run()
        return

    dialog.new_master_password = master_password
    dialog.destroy()


def _on_delete_event(widget, event):
    dialog = widget.get_toplevel()
    dialog.destroy()


def build_change_master_password_dialog():
    handlers = {
        "on_ok_button_pressed": _on_ok_button_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/change_master_password.glade")
    builder.connect_signals(handlers)

    dialog = builder.get_object("ChangeMasterPasswordDialog")
    dialog.connect("delete-event", _on_delete_event)

    dialog.new_master_password = None
    dialog.master_password_entry = builder.get_object("master_password_entry")
    dialog.master_password2_entry = builder.get_object("master_password2_entry")

    return dialog
