from interpreter import Interpreter
from lexer import Lexer
import sys

from parsers import Parser

def main() -> None:
    if len(sys.argv) != 3:
        print(f"[Usage] {sys.argv[0]} <input_file> <output_file>")
        exit(1)

    source_code = ""

    lexer = Lexer(sys.argv[1])
    lexer.lex()
    for token in lexer.output_tokens:
        print(token, "\n")

    print("PARSED: \n")
    parser = Parser(lexer.output_tokens)
    parser.parse()
    for node in parser.output_nodes:
        print(node, "\n")

    interpreter = Interpreter(parser.output_nodes)
    interpreter.interpret()

if __name__ == '__main__':
    main()