from PyQt5.QtCore import QObject, pyqtSignal
from interpreter.run_interpretation_process import run_interpretation_process

class InterpreterController(QObject):

    interpretationFinished = pyqtSignal(object)

    def __init__(self, code_editor, crafting_table, debug_panel, parent=None):
        super().__init__(parent)
        self.code_editor = code_editor
        self.crafting_table = crafting_table
        self.debug_panel = debug_panel

    def interpret_code(self):
        code = self.code_editor.toPlainText()
        self.debug_panel.append_message("Starting interpretation process...")

        abstract_syntax_tree = run_interpretation_process(code)

        if abstract_syntax_tree is not None:
            self.debug_panel.append_message("Interpretation completed successfully.")
            self.interpretationFinished.emit(abstract_syntax_tree)
        else:
            self.debug_panel.append_message("Interpretation failed due to errors.")
