from interpreter.lexical_analyzer.lexer import Lexer, LexicalError
from interpreter.syntax_analyzer.parser import Parser
from interpreter.semantic_analyzer.semantic_analyzer import SemanticAnalyzer
from interpreter.syntax_analyzer.syntax_error import SyntaxError
from interpreter.evaluator.interpreter import Interpreter

def run_interpretation_process(code):
    # ------------- LEXICAL ANALYZER -------------
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
    except LexicalError as le:
        print("Lexical Error:", le)
        return None  # Retornamos None en caso de error
    
    # ------------- SYNTAX ANALYZER -------------
    try:
        parser = Parser(tokens)
        abstract_syntax_tree = parser.parse()  # Se asume que parse() retorna un AST (por ejemplo, un diccionario)
        print("Syntactic analysis completed successfully.")
    except SyntaxError as se:
        print("Syntax Error:", se)
        return None
    
    # ------------- SEMANTIC ANALYZER -------------
    try:
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(abstract_syntax_tree)
        print("Semantic analysis completed successfully.")
    except Exception as e:
        print("Semantic Analysis Error:", e)
        return None

    # ------------- INTERPRETER EVALUATION -------------
    # (Opcional) Si quieres ejecutar el código, puedes hacerlo:
    interpreter = Interpreter()
    interpreter.run(abstract_syntax_tree)
    
    # Extraer la información relevante de la receta para actualizar la mesa de crafteo.
    # Se asume que el AST tiene una estructura con una clave "recipe".
    if isinstance(abstract_syntax_tree, dict) and "recipe" in abstract_syntax_tree:
        recipe_ast = abstract_syntax_tree["recipe"]
    else:
        # Si el AST es directamente la receta o no tiene clave "recipe", retornamos el AST completo.
        recipe_ast = abstract_syntax_tree

    return recipe_ast

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

    recipe bread {
        input: [ (0,0) 1 wheat, (0,1) 1 wheat, (0,2) 1 wheat ];
        output: bread;
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

    func test_semantic_error() {
        log("Testing semantic error: " + undefined_variable);
    }
    """
    ast = run_interpretation_process(code)
    print("AST returned:", ast)
