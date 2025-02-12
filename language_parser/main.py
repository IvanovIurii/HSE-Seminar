from interpreter import Interpreter
from language_parser.tokenizer import Tokenizer
from syntax_tree import parse


def main(code):
    tokenizer = Tokenizer
    tokens = list(tokenizer.tokenize(code))
    ast = parse(tokens)

    interpreter = Interpreter()
    for node in ast.children:
        interpreter.evaluate(node)

    print(interpreter.variables.get('tre'))


code = '''
    As uno = XI + C
    As de = Anagnosi
    As tre = uno + de - L
    Grafo tre
    '''

main(code)
