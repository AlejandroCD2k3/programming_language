from .SyntaxError import SyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        self._parse_program()

    def _parse_program(self):
        while self.position < len(self.tokens):
            if self._peek_lexeme() == "func":
                self._parse_function_definition()
            elif self._peek_lexeme() == "recipe":
                self._parse_recipe_list()
            else:
                self._parse_statement()

    # --------------------- FUNCIONES ---------------------
    def _parse_function_definition(self):
        self._consume("KEYWORD", "func")
        self._consume("IDENTIFIER")
        self._consume("SYMBOL", "(")
        self._parse_parameter_list()
        self._consume("SYMBOL", ")")
        self._consume("SYMBOL", "{")
        self._parse_statement_list()
        self._consume("SYMBOL", "}")

    def _parse_parameter_list(self):
        if self._peek_lexeme() != ")":
            self._consume("IDENTIFIER")
            while self._peek_lexeme() == ",":
                self._consume("SYMBOL", ",")
                self._consume("IDENTIFIER")

    # --------------------- RECETAS ---------------------
    def _parse_recipe_list(self):
        while self.position < len(self.tokens) and self._peek_lexeme() == "recipe":
            self._parse_recipe()

    def _parse_recipe(self):
        self._consume("KEYWORD", "recipe")
        self._consume("IDENTIFIER")
        self._consume("SYMBOL", "{")
        self._parse_recipe_body()
        self._consume("SYMBOL", "}")

    def _parse_recipe_body(self):
        self._parse_input_clause()
        self._consume("SYMBOL", ";")
        self._parse_output_clause()
        self._consume("SYMBOL", ";")
        self._parse_tool_clause()
        self._consume("SYMBOL", ";")
        self._parse_quantity_clause()
        self._consume("SYMBOL", ";")

    def _parse_input_clause(self):
        self._consume("KEYWORD", "input")
        self._consume("SYMBOL", ":")
        self._consume("SYMBOL", "[")
        self._parse_item_list()
        self._consume("SYMBOL", "]")

    def _parse_output_clause(self):
        self._consume("KEYWORD", "output")
        self._consume("SYMBOL", ":")
        self._consume("IDENTIFIER")

    def _parse_tool_clause(self):
        self._consume("KEYWORD", "tool_required")
        self._consume("SYMBOL", ":")
        self._consume("IDENTIFIER")

    def _parse_quantity_clause(self):
        self._consume("KEYWORD", "quantity")
        self._consume("SYMBOL", ":")
        self._consume("NUMBER")

    def _parse_item_list(self):
        self._parse_item()
        while self._peek_lexeme() == ",":
            self._consume("SYMBOL", ",")
            self._parse_item()

    def _parse_item(self):
        self._consume("SYMBOL", "(")
        row = self._consume("NUMBER")    
        self._consume("SYMBOL", ",")
        col = self._consume("NUMBER")      
        self._consume("SYMBOL", ")")
        
        quantity = self._consume("NUMBER")
        material = self._consume("IDENTIFIER")
        
        return {
            "position": (row, col),
            "quantity": quantity,
            "material": material
        }

    def _parse_item_list(self):
        items = [self._parse_item()]
        while self._peek_lexeme() == ",":
            self._consume("SYMBOL", ",")
            items.append(self._parse_item())
        return items

    def _parse_input_clause(self):
        self._consume("KEYWORD", "input")
        self._consume("SYMBOL", ":")
        self._consume("SYMBOL", "[")
        items = self._parse_item_list()
        self._consume("SYMBOL", "]")
        return items


    # --------------------- SENTENCIAS Y ESTRUCTURAS DE CONTROL ---------------------
    def _parse_statement_list(self):
        while self.position < len(self.tokens) and self._peek_lexeme() != "}":
            self._parse_statement()

    def _parse_statement(self):
        token_type, lexeme, _ = self._peek()
        if token_type == "IDENTIFIER":
            if self._lookahead_is_operator("="):
                self._parse_assignment()
            else:
                raise SyntaxError("Sentencia inesperada: se encontró un identificador sin asignación", self._current_position())
        elif token_type == "KEYWORD":
            if lexeme == "if":
                self._parse_conditional()
            elif lexeme in ("while", "for"):
                self._parse_loop()
            elif lexeme == "log":
                self._parse_log_command()
            elif lexeme == "craft":
                self._parse_craft_command()
            else:
                raise SyntaxError(f"Sentencia no válida que inicia con '{lexeme}'", self._current_position())
        else:
            raise SyntaxError("Sentencia no válida", self._current_position())

    def _parse_assignment(self, require_semicolon=True):
        """
        Producción para asignación:
            assignment -> IDENTIFIER '=' expression ';'
        El parámetro require_semicolon permite omitir el consumo del ';' en contextos como el encabezado de un for.
        """
        self._consume("IDENTIFIER")
        self._consume("OPERATOR", "=")
        self._parse_expression()
        if require_semicolon:
            self._consume("SYMBOL", ";")

    def _parse_conditional(self):
        self._consume("KEYWORD", "if")
        self._consume("SYMBOL", "(")
        self._parse_expression()
        self._consume("SYMBOL", ")")
        self._consume("SYMBOL", "{")
        self._parse_statement_list()
        self._consume("SYMBOL", "}")
        if self._peek_lexeme() == "else":
            self._consume("KEYWORD", "else")
            self._consume("SYMBOL", "{")
            self._parse_statement_list()
            self._consume("SYMBOL", "}")

    def _parse_loop(self):
        if self._peek_lexeme() == "while":
            self._consume("KEYWORD", "while")
            self._consume("SYMBOL", "(")
            self._parse_expression()
            self._consume("SYMBOL", ")")
            self._consume("SYMBOL", "{")
            self._parse_statement_list()
            self._consume("SYMBOL", "}")
        elif self._peek_lexeme() == "for":
            self._consume("KEYWORD", "for")
            self._consume("SYMBOL", "(")
            self._parse_assignment(require_semicolon=False)
            self._consume("SYMBOL", ";")
            self._parse_expression()
            self._consume("SYMBOL", ";")
            self._parse_assignment(require_semicolon=False)
            self._consume("SYMBOL", ")")
            self._consume("SYMBOL", "{")
            self._parse_statement_list()
            self._consume("SYMBOL", "}")

    def _parse_log_command(self):
        self._consume("KEYWORD", "log")
        self._consume("SYMBOL", "(")
        self._parse_expression()
        self._consume("SYMBOL", ")")
        self._consume("SYMBOL", ";")

    def _parse_craft_command(self):
        self._consume("KEYWORD", "craft")
        self._consume("KEYWORD", "recipe")
        self._consume("IDENTIFIER")
        self._consume("SYMBOL", ";")

    def _parse_expression(self):
        self._parse_term()
        while self.position < len(self.tokens) and self._peek_type() == "OPERATOR":
            self._consume("OPERATOR")
            self._parse_term()

    def _parse_term(self):
        token_type, lexeme, _ = self._peek()
        if token_type == "NUMBER":
            self._consume("NUMBER")
        elif token_type == "STRING":
            self._consume("STRING")
        elif token_type == "IDENTIFIER":
            self._consume("IDENTIFIER")
        elif token_type == "SYMBOL" and lexeme == "(":
            self._consume("SYMBOL", "(")
            self._parse_expression()
            self._consume("SYMBOL", ")")
        else:
            raise SyntaxError("Término no válido en la expresión", self._current_position())

    # --------------------- FUNCIONES AUXILIARES ---------------------
    def _consume(self, expected_type, expected_lexeme=None):
        if self.position >= len(self.tokens):
            raise SyntaxError("Fin inesperado de la entrada", self._current_position())
        token_type, lexeme, position = self.tokens[self.position]
        if token_type != expected_type or (expected_lexeme is not None and lexeme != expected_lexeme):
            expected_info = f"{expected_type} '{expected_lexeme}'" if expected_lexeme else expected_type
            raise SyntaxError(f"Se esperaba {expected_info}, pero se encontró {token_type} '{lexeme}'", position)
        self.position += 1

    def _peek(self):
        if self.position >= len(self.tokens):
            return None, None, self.position
        return self.tokens[self.position]

    def _peek_type(self):
        return self._peek()[0]

    def _peek_lexeme(self):
        return self._peek()[1]

    def _current_position(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position][2]
        return self.tokens[-1][2] if self.tokens else 0

    def _lookahead_is_operator(self, op):
        """
        Verifica si el token siguiente (lookahead) es un operador específico.
        Esto es útil para distinguir sentencias de asignación cuando el primer token es un identificador.
        """
        if self.position + 1 < len(self.tokens):
            next_token = self.tokens[self.position + 1]
            return next_token[0] == "OPERATOR" and next_token[1] == op
        return False