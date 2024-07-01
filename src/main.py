import functools
import os
import sys

from aqt import gui_hooks, mw
from aqt.browser.browser import Browser
from aqt.qt import *

sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from .config import config
from .errors import setup_error_handler
from .gui.edit import EditNote


def on_shortcut_activated(browser: Browser) -> None:
    for nid in browser.selected_notes():
        EditNote(mw, mw.col.get_note(nid)).show()


def add_browser_shortcut(browser: Browser) -> None:
    shortcut = QShortcut(QKeySequence(config["shortcut"]), browser)
    qconnect(shortcut.activated, functools.partial(on_shortcut_activated, browser))


setup_error_handler()
gui_hooks.browser_will_show.append(add_browser_shortcut)
