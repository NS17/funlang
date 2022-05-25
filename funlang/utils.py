from .tokenizer import parse_string
from .parser import Parser
from .interpreter import Interpreter


def run_code(input_string: str) -> float:
    """
    Tokenizes, parses and executes code in the input string
    :param input_string: string with code
    :return: final value
    """
    tokens = list(parse_string(input_string))
    ast = Parser(tokens).parse_main()
    interpreter = Interpreter()
    return interpreter.execute(ast)
