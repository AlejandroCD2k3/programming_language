from lexicalAnalizer.Lexeme import TOKEN_PATTERNS
from lexicalAnalizer.Lexer import Lexer, LexicalError
from syntaxAnalizer.Parser import Parser
from syntaxAnalizer.SyntaxError import SyntaxError
import numpy

def main():

    code = """
        func calculate_area(length, width) {
    result = length * width;
    if (result > 100) {
        log("Large area calculated");
    } else {
        log("Small area calculated");
    }
    }

    recipe cake {
        input: [2 sugar, 1 flour];
        output: cake;
        tool_required: oven;
        quantity: 1;
    }

func greet_user(name) {
    log("Hello");
}

func countdown(number) {
    while (number > 0) {
        log("Countdown:");
        number = number - 1;
    }
    log("Countdown finished");
}

func repeat_task(times) {
    for (i = 1; i <= times; i = i + 1;) {
        log("Task repetition #");
    }
}
"""
 
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    try:
        parser.parse()
        print("El código es válido.")
    except SyntaxError as e:
        print(e)
    
    try:
        tokens = lexer.tokenize()
        print("\nTokens found:")
        print("-------------------")
        for token in tokens:
            print(f"Type: {token[0]}, Lexeme: '{token[1]}', Position: {token[2]}")
    except LexicalError as lexical_error:
        print(lexical_error)

if __name__ == "__main__":
    main()