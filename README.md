# Programming Language

This repository demonstrates the structure of a custom programming language designed with a Minecraft-themed crafting system. The project covers every stage of a typical compilation pipeline:

- **Lexical Analysis (Lexer)**
- **Syntactic Analysis (Parser)**
- **Semantic Analysis**
- **Interpretation / Evaluation (Interpreter)**
- **Controllers**
- **Graphical User Interface (GUI)**

Each module has been designed to operate independently, while the entire system integrates seamlessly to transform source code into dynamic, executable behavior.

---

## Lexical Analyzer

Lexical analysis is one of the first and most critical stages in the implementation of our Minecraft programming language. Its role is essential in transforming source code into a tokenized representation that can be processed by subsequent stages, such as the parser. The lexer operates by breaking down the source code into tokens, adhering to the token patterns established for our language. At the same time, it performs error detection—identifying lexical issues like invalid characters or malformed symbols—thereby ensuring that the input code adheres to the foundational rules of the language, paving the way for smoother syntactic analysis.

```python
from .lexeme import TOKEN_PATTERNS
from .lexical_error import LexicalError
import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.code):
            match_found = self._match_next_token()
            if not match_found:
                self._handle_invalid_character()
        return self.tokens

    def _match_next_token(self):
        for token_name, pattern in TOKEN_PATTERNS:
            match = pattern.match(self.code, self.position)
            if match:
                lexeme = match.group()
                position = self.position
                self.position = match.end()
                
                self._validate_token(token_name, lexeme, position)

                if token_name not in ("WHITESPACE", "COMMENT"):
                    self.tokens.append((token_name, lexeme, position))
                return True
        return False

    def _validate_token(self, token_name, lexeme, position):
        if token_name == "STRING" and not lexeme.endswith('"'):
            raise LexicalError("Unterminated string literal", position)
        elif token_name == "NUMBER":
            try:
                float(lexeme)
            except ValueError:
                raise LexicalError("Number literal overflow or invalid format", position)

    def _handle_invalid_character(self):
        current_char = self.code[self.position]
        position = self.position
        
        if current_char.isprintable():
            raise LexicalError(f"Invalid character '{current_char}'", position)
        else:
            raise LexicalError("Non-printable character detected", position)
```

## Constructor (Lexical Analyzer)

### `__init__(self, code)`
Initializes the lexer with the source code to be analyzed. It sets the initial position to `0` and creates an empty list to store the tokens found in the code.

### `tokenize(self)`
- This is the main function that iterates over the source code.
- For each position, it calls `_match_next_token()` to try to match a valid token.
- If no valid token is found at the current position, it calls `_handle_invalid_character()`.
- Finally, it returns the list of tokens collected.

### `_match_next_token(self)`
- Iterates through the defined token patterns in `TOKEN_PATTERNS` and attempts to match a token at the current position in the code.
- If a match is found:
  - The lexeme is extracted.
  - The current position is updated to the end of the matched lexeme.
  - The token is validated using `_validate_token()`.
  - If the token is not a `WHITESPACE` or `COMMENT`, it is appended to the `tokens` list (along with its type and starting position).
- If no token matches, the method returns `False`.

### `_validate_token(self, token_name, lexeme, position)`
- Validates tokens with specific requirements:
  - For a `STRING` token, if the lexeme does not end with a quotation mark (`"`), it raises a lexical error indicating an unterminated string.
  - For a `NUMBER` token, it attempts to convert the lexeme to a float. If the conversion fails (due to overflow or invalid format), it raises a lexical error.

### `_handle_invalid_character(self)`
- When no valid token is matched at the current position, this method retrieves the current character and its position.
- If the character is **printable**, it raises a lexical error indicating an **invalid character**.
- Otherwise, it raises an error indicating that a **non-printable character** was detected.

---

## Syntactic Analyzer

Syntactic analysis transforms the **stream of tokens** produced by the lexer into a **hierarchical structure**, typically an **Abstract Syntax Tree (AST)**.  
The parser verifies that the tokens conform to the **language's grammar** by checking constructs such as:

- **Function definitions**
- **Recipes**
- **Assignments**
- **Control structures**

This organized **AST structure** is essential for further **semantic analysis and evaluation**.  
The parser also detects **syntax errors** (e.g., missing delimiters, unexpected tokens) and **prevents invalid code** from progressing to subsequent stages.

---

## Semantic Analyzer

Semantic analysis checks the **AST for semantic correctness** beyond mere syntax. It ensures that:

- **Variables and functions** are declared before use.
- **Operations** are applied to **compatible types**.
- **Specific language rules** (such as valid index ranges for recipe inputs) are respected.

Using a **visitor pattern**, the semantic analyzer **traverses the AST** and raises **custom semantic errors** when violations are detected.  
This guarantees that the code is **logically consistent before interpretation**.

---

## Interpreter / Evaluation Process

The **interpreter** takes the **semantically validated AST** and executes it. It:

- **Evaluates expressions**
- **Processes assignments**
- **Handles control structures** (such as conditionals, loops, and function calls)
- **Updates a global environment** with variables, functions, and recipes

This phase **turns the static AST into dynamic, executable behavior**, providing **immediate feedback** and a **simulation of in-game crafting operations**.

---

## Controllers

Controllers serve as the **bridge** between the **GUI** and the **core language processing pipeline**.  
The primary controller, `InterpreterController`:

- Retrieves **source code** from the **code editor**.
- Initiates the **interpretation process** (which includes lexical, syntactic, and semantic analysis).
- Updates the **crafting table** with the results.
- Handles **error reporting** by capturing exceptions from each phase and displaying **detailed messages** in the **debug panel**.
- Emits **signals** to notify other components when **interpretation completes successfully**.

---

## Graphical User Interface (GUI)

The **GUI** provides an interactive environment for **writing, testing, and visualizing code**. It consists of several key components:

- **Code Editor**: A text editor with **syntax highlighting** tailored for our **Minecraft programming language**.
- **Debug Panel**: A pane that displays **real-time logs, error messages, and debugging output**.
- **Crafting Table Widget**: A **visual simulation of a 3x3 crafting grid** that updates based on recipe data.
- **Template Panel**: A panel that allows users to **quickly insert pre-defined recipe templates** into the code editor.

The **GUI** is organized into **left and right panels** with distinct **color schemes**, creating a **clear and user-friendly layout**.  
This **integration** ensures that any **change in the code** is promptly **reflected in both the visual crafting table and the debug output**.

---

## Troubleshooting

### PyQt5 Dependencies
If you encounter the following error:

ModuleNotFoundError: No module named 'PyQt5'

Install PyQt5 using:

```sh
python -m pip install PyQt5

## Docker and Qt Platform Plugin Issues
For Docker deployments, ensure that necessary system libraries are installed (libx11-6, libxcb1, libfontconfig1, etc.) and that the X11 socket is correctly mounted.

docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix programming-language

## ProjectStructure

programming_language/
├── README.md
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── main.py
├── interpreter/
│   ├── lexical_analyzer/
│   │   ├── lexeme.py
│   │   └── lexical_error.py
│   ├── syntax_analyzer/
│   │   ├── parser.py
│   │   └── syntax_error.py
│   ├── semantic_analyzer/
│   │   ├── semantic_analyzer.py
│   │   └── semantic_error.py
│   └── evaluator/
│       └── interpreter.py
├── controller/
│   └── interpreter_controller.py
├── run_interpretation_process.py
└── gui/
│   ├── code_editor.py
│   ├── debug_panel.py
│   ├── crafting_table.py
│   └── template_panel.py
└── templates/
