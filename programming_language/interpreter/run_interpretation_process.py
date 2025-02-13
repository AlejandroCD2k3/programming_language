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
        print(le)
        return
    
    # ------------- SYNTAX ANALYZER -------------

    try:
        parser = Parser(tokens)
        abstract_syntax_tree = parser.parse()
        print("Syntactic analysis completed successfully.")
    except SyntaxError as se:
        print(se)
        return
    
    # ------------- SEMANTIC ANALYZER -------------

    try:
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(abstract_syntax_tree)
        print("Semantic analysis completed successfully.")
    except Exception as e:
        print(e)
        return

    # ------------- INTERPRETER EVALUATION -------------

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

    run_interpretation_process(code)
