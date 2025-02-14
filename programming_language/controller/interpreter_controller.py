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

        recipe_ast = run_interpretation_process(code)
        if recipe_ast is None:
            self.debug_panel.append_message("Interpretation failed due to errors.")
            return

        # Si el AST es una lista, tomamos el primer elemento
        if isinstance(recipe_ast, list):
            if len(recipe_ast) > 0:
                recipe_ast = recipe_ast[0]
            else:
                self.debug_panel.append_message("No recipes found in the code.")
                return

        # Actualizar la mesa de crafteo con el AST obtenido
        self.crafting_table.update_from_ast(recipe_ast)
        self.debug_panel.append_message("Interpretation completed successfully.")
        self.interpretationFinished.emit(recipe_ast)
