import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def _on_ok_button_pressed(button):
    dialog = button.get_toplevel()
    dialog.destroy()


def _on_delete_event(widget, event):
    dialog = widget.get_toplevel()
    dialog.destroy()


def build_error_dialog(error_message: str):
    handlers = {
        "on_ok_button_pressed": _on_ok_button_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/error.glade")
    builder.connect_signals(handlers)

    dialog = builder.get_object("ErrorDialog")
    dialog.connect("delete-event", _on_delete_event)

    error_message_label = builder.get_object("error_message_label")
    error_message_label.set_text(error_message)

    return dialog
