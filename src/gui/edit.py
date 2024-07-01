import aqt.editor
from anki.notes import Note
from aqt import gui_hooks
from aqt.editcurrent import EditCurrent
from aqt.main import AnkiQt
from aqt.qt import *
from aqt.utils import restoreGeom, tr


class EditNote(EditCurrent):
    # pylint: disable=super-init-not-called
    def __init__(self, mw: AnkiQt, note: Note) -> None:
        # pylint: disable=non-parent-init-called
        QMainWindow.__init__(self, None, Qt.WindowType.Window)
        self.mw = mw
        self.form = aqt.forms.editcurrent.Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(tr.editing_edit_current())
        self.setMinimumHeight(400)
        self.setMinimumWidth(250)
        self.editor = aqt.editor.Editor(
            self.mw,
            self.form.fieldsArea,
            self,
            editor_mode=aqt.editor.EditorMode.EDIT_CURRENT,
        )
        self.note = note
        self.editor.card = self.note.cards()[0]
        self.editor.set_note(self.note, focusTo=0)
        restoreGeom(self, "editcurrent")
        close_button = self.form.buttonBox.button(QDialogButtonBox.StandardButton.Close)
        close_button.setShortcut(QKeySequence("Ctrl+Return"))
        # qt5.14+ doesn't handle numpad enter on Windows
        self.compat_add_shorcut = QShortcut(QKeySequence("Ctrl+Enter"), self)
        qconnect(self.compat_add_shorcut.activated, close_button.click)
        gui_hooks.operation_did_execute.append(self.on_operation_did_execute)
