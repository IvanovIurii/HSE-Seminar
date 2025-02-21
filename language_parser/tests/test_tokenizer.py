import unittest
from language_parser.tokenizer import Tokenizer
from language_parser.tokenizer.consts import (
    FUNC,
    IDENTIFIER,
    PLUS,
    EQ,
    NEWLINE,
    NUMBER,
    OUT,
    ASSIGN,
    IN,
    BRANCH,
    LP,
    MINUS,
    RP
)
from language_parser.tokenizer.tokenizer import Token


class TestTokenizer(unittest.TestCase):

    def test_should_tokenize(self):
        code = '''
            As uno = XI + C
            As de = Anagnosi
            As tre = uno + de
            Grafo tre
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)

        expected_tokens = [
            Token(ASSIGN, "As"),
            Token(IDENTIFIER, "uno"),
            Token(EQ, "="),
            Token(NUMBER, "XI"),
            Token(PLUS, "+"),
            Token(NUMBER, "C"),
            Token(NEWLINE, "\n"),

            Token(ASSIGN, "As"),
            Token(IDENTIFIER, "de"),
            Token(EQ, "="),
            Token(IN, "Anagnosi"),
            Token(NEWLINE, "\n"),

            Token(ASSIGN, "As"),
            Token(IDENTIFIER, "tre"),
            Token(EQ, "="),
            Token(IDENTIFIER, "uno"),
            Token(PLUS, "+"),
            Token(IDENTIFIER, "de"),
            Token(NEWLINE, "\n"),

            Token(OUT, "Grafo"),
            Token(IDENTIFIER, "tre"),
            Token(NEWLINE, "\n")
        ]

        self.assertListEqual(tokens, expected_tokens)

    def test_should_tokenize_sum_function(self):
        code = '''
            Munus sum a b = a + b
            As computo = sum XI C
            Grafo computo
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)

        expected_tokens = [
            Token(FUNC, "Munus"),
            Token(IDENTIFIER, "sum"),
            Token(IDENTIFIER, "a"),
            Token(IDENTIFIER, "b"),
            Token(EQ, "="),
            Token(IDENTIFIER, "a"),
            Token(PLUS, "+"),
            Token(IDENTIFIER, "b"),
            Token(NEWLINE, "\n"),

            Token(ASSIGN, "As"),
            Token(IDENTIFIER, "computo"),
            Token(EQ, "="),
            Token(IDENTIFIER, "sum"),
            Token(NUMBER, "XI"),
            Token(NUMBER, "C"),
            Token("NEWLINE", "\n"),

            Token(OUT, "Grafo"),
            Token(IDENTIFIER, "computo"),
            Token(NEWLINE, "\n"),
        ]

        self.assertListEqual(tokens, expected_tokens)

    def test_should_tokenize_ternary(self):
        code = '''
            Munus fib n = Sinon n I ((fib n - I) + (fib n - II))
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)

        expected_tokens = [
            Token(FUNC, "Munus"),
            Token(IDENTIFIER, "fib"),
            Token(IDENTIFIER, "n"),
            Token(EQ, "="),
            Token(BRANCH, "Sinon"),
            Token(IDENTIFIER, "n"),
            Token(NUMBER, "I"),
            Token(LP, "("),
            Token(LP, "("),
            Token(IDENTIFIER, "fib"),
            Token(IDENTIFIER, "n"),
            Token(MINUS, "-"),
            Token(NUMBER, "I"),
            Token(RP, ")"),
            Token(PLUS, "+"),
            Token(LP, "("),
            Token(IDENTIFIER, "fib"),
            Token(IDENTIFIER, "n"),
            Token(MINUS, "-"),
            Token(NUMBER, "II"),
            Token(RP, ")"),
            Token(RP, ")"),
            Token(NEWLINE, "\n"),
        ]

        self.assertListEqual(tokens, expected_tokens)
