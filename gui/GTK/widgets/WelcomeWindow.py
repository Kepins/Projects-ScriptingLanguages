import gi

from widgets.AboutAppDialog import build_about_app_dialog
from widgets.CreatePassDBDialog import build_create_pass_db_dialog
from widgets.OpenPassDBDialog import build_open_pass_db_dialog

# from widgets.AboutAppDialog import AboutAppDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def _on_about_app_pressed(widget):
    print("About app button clicked")

    about_dialog = build_about_app_dialog()
    about_dialog.run()


def _on_create_pass_db_pressed(widget):
    print("Create pass db button clicked")
    dialog = build_create_pass_db_dialog()
    dialog.run()

    print(dialog.auto_saving_manager)


def _on_open_pass_db_pressed(widget):
    print("Open pass db button clicked")
    dialog = build_open_pass_db_dialog()
    dialog.run()

    print(dialog.auto_saving_manager)


def _on_close_app_pressed(widget):
    print("Exit button clicked")
    Gtk.main_quit()


def build_welcome_window():
    handlers = {
        "on_about_app_pressed": _on_about_app_pressed,
        "on_create_pass_db_pressed": _on_create_pass_db_pressed,
        "on_open_pass_db_pressed": _on_open_pass_db_pressed,
        "on_close_app_pressed": _on_close_app_pressed,
    }

    builder = Gtk.Builder()
    builder.add_from_file("ui/welcome_screen.glade")
    builder.connect_signals(handlers)

    return builder.get_object("WelcomeWindow")
