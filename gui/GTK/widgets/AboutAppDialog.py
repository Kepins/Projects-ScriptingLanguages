import gi


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def _on_ok_button_pressed(button):
    dialog = button.get_toplevel()
    dialog.destroy()


def build_about_app_dialog():
    handlers = {
        "on_ok_button_pressed": _on_ok_button_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/about_application.glade")
    builder.connect_signals(handlers)

    return builder.get_object("AboutAppDialog")
