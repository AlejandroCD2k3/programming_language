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
            else:
                self._parse_recipe_list()

    def _parse_function_definition(self):
        self._consume("KEYWORD", "func")
        self._consume("IDENTIFIER")  # Function name
        self._consume("SYMBOL", "(")
        self._parse_parameter_list()  # If your functions have parameters
        self._consume("SYMBOL", ")")
        self._consume("SYMBOL", "{")
        self._parse_statement_list()  # Statements inside the function body
        self._consume("SYMBOL", "}")

    def _parse_parameter_list(self):
        if self._peek_lexeme() != ")":
            self._consume("IDENTIFIER")  # Parameter name
            while self._peek_lexeme() == ",":
                self._consume("SYMBOL", ",")
                self._consume("IDENTIFIER")  # Next parameter

    # Recipe production rules
    def _parse_recipe_list(self):
        self._parse_recipe()
        while self._peek_type() == "KEYWORD" and self._peek_lexeme() == "recipe":
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
        self._consume("NUMBER")
        self._consume("IDENTIFIER")

    # Control structures production rules
    def _parse_statement_list(self):
        self._parse_statement()
        while self._peek_type() == "IDENTIFIER" or self._peek_type() == "KEYWORD":
            self._parse_statement()

    def _parse_statement(self):
        if self._peek_type() == "IDENTIFIER":
            self._parse_assignment()
        elif self._peek_lexeme() == "if":
            self._parse_conditional()
        elif self._peek_lexeme() in ["while", "for"]:
            self._parse_loop()
        elif self._peek_lexeme() == "log":
            self._parse_log_command()
        elif self._peek_lexeme() == "craft":
            self._parse_craft_command()
        else:
            raise SyntaxError("Invalid statement", self._current_position())

    def _parse_assignment(self):
        self._consume("IDENTIFIER")
        self._consume("OPERATOR", "=")
        self._parse_expression()
        if(self._peek_lexeme() != ")"):
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
            self._parse_assignment()
            self._parse_expression()
            self._consume("SYMBOL", ";")
            self._parse_assignment()
            self._consume("SYMBOL", ")")
            self._consume("SYMBOL", "{")
            self._parse_statement_list()
            self._consume("SYMBOL", "}")

    def _parse_log_command(self):
        self._consume("KEYWORD", "log")
        self._consume("SYMBOL", "(")
        self._consume("STRING")
        self._consume("SYMBOL", ")")
        self._consume("SYMBOL", ";")

    def _parse_craft_command(self):
        self._consume("KEYWORD", "craft")
        self._consume("KEYWORD", "recipe")
        self._consume("IDENTIFIER")
        self._consume("SYMBOL", ";")

    def _parse_expression(self):
        self._parse_term()
        while self._peek_type() == "OPERATOR":
            self._consume("OPERATOR")
            self._parse_term()

    def _parse_term(self):
        if self._peek_type() == "NUMBER":
            self._consume("NUMBER")
        elif self._peek_type() == "IDENTIFIER":
            self._consume("IDENTIFIER")
        else:
            raise SyntaxError("Invalid term in expression", self._current_position())

    # Utility functions
    def _consume(self, expected_type, expected_lexeme=None):
        if self.position >= len(self.tokens):
            raise SyntaxError("Unexpected end of input", self._current_position())

        token_type, lexeme, position = self.tokens[self.position]
        if token_type != expected_type or (expected_lexeme and lexeme != expected_lexeme):
            raise SyntaxError(f"Expected {expected_type} {expected_lexeme or ''}, got {token_type} '{lexeme}'", position)

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
        return self.tokens[self.position][2] if self.position < len(self.tokens) else len(self.tokens)