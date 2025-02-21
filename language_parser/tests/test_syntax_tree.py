import unittest

from language_parser.syntax_tree import parse
from language_parser.tokenizer import Tokenizer


class TestSyntaxTree(unittest.TestCase):
    def test_should_build_ast_for_function_declaration(self):
        code = '''
            Munus sum a b c = a + b + c
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_numbers(self):
        code = '''
            As uno = XI + C + I
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_function_invocation(self):
        code = '''
            As computo = sum XI C I
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_function_invocation_with_op(self):
        code = '''
            As computo = sum XI + L
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_function_invocation_with_op_and_parenthesis(self):
        code = '''
            As computo = sum XI (D + L)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_ops_with_parenthesis(self):
        code = '''
            As computo = XI + (D - L)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_function_inside_with(self):
        code = '''
            As sum = XI + (min a b)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()
