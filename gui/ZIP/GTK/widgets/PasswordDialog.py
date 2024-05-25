from enum import Enum

import gi

from password_manager.manager import AddUpdatePasswordEntry, PasswordEntry
from widgets.ErrorDialog import build_error_dialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class STATES(Enum):
    SHOWING = 0
    EDITING = 1


def _on_save_edit_button_pressed(button):
    dialog = button.get_toplevel()

    if dialog.state == STATES.SHOWING:
        print("Edit button clicked")
        _change_state(dialog, STATES.EDITING)
    elif dialog.state == STATES.EDITING:
        print("Save button clicked")

        name = dialog.name_entry.get_text()
        username = dialog.username_entry.get_text()
        password = dialog.password_entry.get_text()

        if not name or not username or not password:
            build_error_dialog(error_message="Wypełnij wszystkie pola!").run()
            return

        dialog.add_update_password_entry = AddUpdatePasswordEntry(
            name=name, username=username, password=password
        )
        _change_state(dialog, STATES.SHOWING)



def _on_cancel_button_pressed(button):
    dialog = button.get_toplevel()

    print("Cancel button clicked")
    _change_state(dialog, STATES.SHOWING)


def _on_delete_event(widget, event):
    dialog = widget.get_toplevel()
    dialog.destroy()


def _change_state(dialog, state: STATES):
    dialog.state = state

    dialog.name_entry.set_text(dialog.add_update_password_entry.name)
    dialog.username_entry.set_text(dialog.add_update_password_entry.username)
    dialog.password_entry.set_text(dialog.add_update_password_entry.password)
    if state == STATES.SHOWING:
        dialog.save_edit_button.set_label("Edytuj")
        dialog.cancel_button.hide()
        dialog.name_entry.set_property("editable", False)
        dialog.username_entry.set_property("editable", False)
        dialog.password_entry.set_property("editable", False)
    if state == STATES.EDITING:
        dialog.save_edit_button.set_label("Zapisz")
        dialog.cancel_button.show()
        dialog.name_entry.set_property("editable", True)
        dialog.username_entry.set_property("editable", True)
        dialog.password_entry.set_property("editable", True)


def build_password_dialog(password_entry: PasswordEntry, state: STATES):
    handlers = {
        "on_save_edit_button_pressed": _on_save_edit_button_pressed,
        "on_cancel_button_pressed": _on_cancel_button_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/password_dialog.glade")
    builder.connect_signals(handlers)

    dialog = builder.get_object("PasswordDialog")
    dialog.connect("delete-event", _on_delete_event)

    dialog.add_update_password_entry = AddUpdatePasswordEntry(
        name=password_entry.name, username=password_entry.username, password=password_entry.password
    )
    dialog.name_entry = builder.get_object("name_entry")
    dialog.username_entry = builder.get_object("username_entry")
    dialog.password_entry = builder.get_object("password_entry")

    dialog.save_edit_button = builder.get_object("save_edit_button")
    dialog.cancel_button = builder.get_object("cancel_button")

    _change_state(dialog,  state)


    return dialog