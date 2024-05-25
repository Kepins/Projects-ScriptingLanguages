import gi

from widgets.WelcomeWindow import build_welcome_window

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if __name__ == "__main__":
    win = build_welcome_window()
    win.show_all()
    Gtk.main()
