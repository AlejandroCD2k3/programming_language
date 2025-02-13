import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from gui.code_editor import CodeEditor
from gui.debug_panel import DebugPanel
from gui.crafting_table import CraftingTableWidget
from gui.template_panel import TemplatePanel
from controller.interpreter_controller import InterpreterController

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Minecraft Crafting Interpreter")
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.code_editor = CodeEditor()
        self.debug_panel = DebugPanel()
        left_layout.addWidget(self.code_editor)
        left_layout.addWidget(self.debug_panel)

        self.run_button = QPushButton("Run Code")
        self.run_button.clicked.connect(self.run_code)
        left_layout.addWidget(self.run_button)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.crafting_table = CraftingTableWidget()
        self.template_panel = TemplatePanel("templates", self.code_editor)
        right_layout.addWidget(self.crafting_table)
        right_layout.addWidget(self.template_panel)

        main_layout.addWidget(left_panel, 2) 
        main_layout.addWidget(right_panel, 1)

        self.interpreter_controller = InterpreterController(self.code_editor, self.crafting_table, self.debug_panel)

    def run_code(self):
        self.interpreter_controller.interpret_code()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())