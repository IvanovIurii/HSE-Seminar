import unittest

from language_parser.syntax_tree.syntax_tree import parse
from language_parser.tokenizer import Tokenizer
from language_parser.tokenizer.consts import FUNC, IDENTIFIER, EQ, PLUS


class TestSyntaxTree(unittest.TestCase):
    def test_should_build_ast_for_function_declaration(self):
        code = '''
            Munus sum a b c = a + b + c
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        func = ast.children[0]

        self.assertEquals(func.type, FUNC)
        self.assertEquals(func.children[0].type, IDENTIFIER)
        self.assertEquals(func.children[0].value, 'sum')

        self.assertEquals(func.children[1].type, EQ)
        self.assertEquals(func.children[2].type, PLUS)

        self.assertEquals(func.children[2].children[0].type, PLUS)
        self.assertEquals(func.children[2].children[1].type, IDENTIFIER)
        self.assertEquals(func.children[2].children[1].value, 'c')

        self.assertEquals(func.children[2].children[0].children[0].type, IDENTIFIER)
        self.assertEquals(func.children[2].children[0].children[0].value, 'a')

        self.assertEquals(func.children[2].children[0].children[1].type, IDENTIFIER)
        self.assertEquals(func.children[2].children[0].children[1].value, 'b')

    def test_should_build_ast_for_numbers(self):
        code = '''
            As uno = XI + C
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_function_invocation(self):
        code = '''
            As duo = sum XI I
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    # should be:
    #
    # CALL: sum
    #   ID a
    #   PLUS: +
    #       NUMBER: I
    #       NUMBER: XI
    def test_should_build_ast_for_function_invocation_sum_first(self):
        code = '''
            As duo = sum a (I + XI)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.to_mermaid_markdown("Sum")

    def test_should_build_ast_for_function_invocation_with_op_and_parenthesis(self):
        code = '''
            As tres = sum XI (D + L)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_ops_with_parenthesis(self):
        code = '''
            As quatro = XI + (D - L)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_function_inside_with(self):
        code = '''
            As minimum = XI + (min a b)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_assign_one_roman_number(self):
        code = '''
            As uno = X
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.print_recursively()

    def test_should_build_ast_for_ternary_operator_statement(self):
        code = '''
            Munus fib n = Sinon n I ((fib (n - I)) + (fib (n - II)))
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        # todo fix mermaid for branch
        ast.to_mermaid_markdown("Sinon")

    def test_foo(self):
        code = '''
            As foo = fib (n - I)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        # todo fix mermaid for branch
        ast.to_mermaid_markdown("Assign fib")
