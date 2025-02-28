import unittest

from language_parser.interpreter import Interpreter
from language_parser.syntax_tree.syntax_tree import parse
from language_parser.tokenizer import Tokenizer


class TestInterpreter(unittest.TestCase):
    def test_should_return_21(self):
        code = '''
            Munus sum a b c = a + b + c
            As computo = sum X X I
            Grafo computo
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 21)

    def test_should_return_an_error(self):
        code = '''
            Munus sum a b c = a + b + c
            As computo = sum X X
            Grafo computo
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()

        # todo: read doc how to use this
        with self.assertRaises(ValueError) as cm:
            interpreter.interpret(ast)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Function 'sum' expects 3 arguments, got 2")

    # NOTE: this is for the sake of testing, we get a result of latest statement as value
    def test_should_add(self):
        code = '''
            As uno = XI + C
        '''

        # todo: print only when GRAFO!!!
        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEqual(result, 111)

    def test_should_subtract(self):
        code = '''
            As uno = C - I
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEqual(result, 99)

    def test_should_return_6(self):
        code = '''
            As uno = V - II + III
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 6)

    def test_should_return_0(self):
        code = '''
            As uno = V - (II + III)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 0)

    def test_should_build_ast_for_function_invocation_sum_first(self):
        code = '''
            As duo = sum a (I + XI)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        pass

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

        ast.to_mermaid_markdown("Sinon")

    def test_foo(self):
        code = '''
            As foo = fib (n - I)
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        ast.to_mermaid_markdown("Assign fib")
