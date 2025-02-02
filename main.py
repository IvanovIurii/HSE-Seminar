from interpreter import Interpreter
from syntax_tree import parse
from tokenizer import tokenize


def main(code):
    tokens = list(tokenize(code))
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
