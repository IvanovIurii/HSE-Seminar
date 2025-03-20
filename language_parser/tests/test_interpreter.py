import unittest

from language_parser.interpreter.interpreter import Interpreter
from language_parser.syntax_tree.syntax_tree import parse
from language_parser.tokenizer import Tokenizer


class TestInterpreter(unittest.TestCase):
    def test_should_return_21(self):
        code = '''
            Munus sum a b c = a + b + c
            As computo = sum X X I
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, "XXI")

    def test_should_return_an_error(self):
        code = '''
            Munus sum a b c = a + b + c
            As computo = sum X X
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()

        with self.assertRaises(ValueError) as cm:
            interpreter.interpret(ast)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Function 'sum' expects 3 arguments, got 2")

    def test_should_add(self):
        code = '''
            As uno = XI + C
            Grafo uno
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEqual(result, "CXI")

    def test_should_subtract(self):
        code = '''
            As uno = C - I
            Grafo uno
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEqual(result, "XCIX")

    def test_should_return_6(self):
        code = '''
            As uno = V - II + III
            Grafo uno
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, "VI")

    def test_should_return_0(self):
        code = '''
            As uno = V - (II + III)
            Grafo uno
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, "N")

    def test_should_throw_an_error_on_undefined_function(self):
        code = '''
            As duo = sum a
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        with self.assertRaises(ValueError) as cm:
            interpreter.interpret(ast)

        the_exception = cm.exception
        self.assertEqual(the_exception.args[0], "Undefined function 'sum'")

    def test_should_build_ast_for_ternary_operator_statement(self):
        code = '''
            Munus fib n = Sinon n I ((fib (n - I)) + (fib (n - II)))
            As fibonacci = fib III
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)

        ast = parse(tokens)
        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        print(result)

    def test_foo(self):
        code = '''
            Munus fun = X + X
            Grafo fun
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 'XX')

    def test_print_X(self):
        code = '''
            Munus func = X
            Grafo func
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 'X')

    def test_double_input_when_X_II(self):
        code = '''
            Munus sum a b = a + b
            As uno = sum Anagnosi Anagnosi 
            Grafo uno
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 'XII')

    def test_input_when_single_V(self):
        code = '''
            As uno = Anagnosi 
            Grafo uno
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 'V')

    def test_double_input_when_I_I(self):
        code = '''
            Munus sum a b = a + b
            Grafo sum Anagnosi Anagnosi 
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 'II')

    def test_should_sum_with_multiple_functions_declaration(self):
        code = '''
            Munus ten = X
            Munus sum a b = a + b
            Grafo sum ten ten
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 'XX')

    def test_should_sum_when_nested(self):
        code = '''
            Munus sum a b = a + b
            Grafo sum (sum X I) II
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)
        ast = parse(tokens)

        interpreter = Interpreter()
        result = interpreter.interpret(ast)

        self.assertEquals(result, 'XIII')
