# interpreter/run_interpretation_process.py

from lexical_analizer.lexer import Lexer, LexicalError
from syntax_analizer.parser import Parser
from syntax_analizer.syntax_error import SyntaxError
from evaluator.interpreter import Interpreter

def run_interpretation_process(code):

    """
    Orchestrates the interpretation process:
      1. Lexical analysis: tokenizes the input code.
      2. Syntactic analysis: builds an Abstract Syntax Tree (AST).
      3. Evaluation: traverses and executes the AST.
    
    Args:
        code (str): The source code to interpret.
    
    Returns:
        The generated AST, if the process is successful.

    """

    # --------------- LEXICAL ANALYSIS ---------------

    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        """
        print("\nTokens found:")
        print("-------------------")
        for token in tokens:
            print(f"Type: {token[0]}, Lexeme: '{token[1]}', Position: {token[2]}")
        """

    except LexicalError as lexical_error:
        print(lexical_error)
        return
    
    # --------------- SYNTAX ANALYSIS ---------------

    try:
        parser = Parser(tokens)
        abstract_syntax_tree = parser.parse()
        print("The code is valid.")
    except SyntaxError as syntax_error:
        print(syntax_error)
        return

    # --------------- INTERPRETATION OF THE ABSTRACT SYNTAX TREE ---------------

    interpreter = Interpreter()
    interpreter.run(abstract_syntax_tree)
    return abstract_syntax_tree

if __name__ == "__main__":
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
        input: [ (0,0) 1 milk_bucket, (0,1) 1 milk_bucket, (0,2) 1 milk_bucket,
                 (1,0) 1 sugar,        (1,1) 1 egg,         (1,2) 1 sugar,
                 (2,0) 1 wheat,        (2,1) 1 wheat,       (2,2) 1 wheat ];
        output: cake;
        tool_required: crafting_table;
        quantity: 1;
    }

    recipe bread {
        input: [ (0,0) 1 wheat, (0,1) 1 wheat, (0,2) 1 wheat ];
        output: bread;
        tool_required: crafting_table;
        quantity: 1;
    }

    recipe wooden_pickaxe {
        input: [ (0,0) 1 wood_plank, (0,1) 1 wood_plank, (0,2) 1 wood_plank,
                 (1,1) 1 stick,
                 (2,1) 1 stick ];
        output: wooden_pickaxe;
        tool_required: crafting_table;
        quantity: 1;
    }

    recipe furnace {
        input: [ (0,0) 1 cobblestone, (0,1) 1 cobblestone, (0,2) 1 cobblestone,
                 (1,0) 1 cobblestone,                           (1,2) 1 cobblestone,
                 (2,0) 1 cobblestone, (2,1) 1 cobblestone, (2,2) 1 cobblestone ];
        output: furnace;
        tool_required: crafting_table;
        quantity: 1;
    }

    func greet_user(name) {
        log("Hello, " + name);
    }

    func countdown(number) {
        while (number > 0) {
            log("Countdown: " + number);
            number = number - 1;
        }
        log("Countdown finished");
    }

    func repeat_task(times) {
        for (i = 1; i <= times; i = i + 1) {
            log("Task repetition #" + i);
        }
    }
    """
    run_interpretation_process(code)
