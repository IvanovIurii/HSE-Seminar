import unittest
from language_parser.tokenizer import Tokenizer
from language_parser.tokenizer.tokenizer import Token


class TestTokenizer(unittest.TestCase):

    # Munus sum a b = a + b

    def test_should_tokenize_sum_function(self):
        code = '''
            Munus sum a b = a + b
            As computo = sum XI C
            Grafo computo
        '''

        tokenizer = Tokenizer
        tokens = tokenizer.tokenize(code)

        # assumption: function name is also lowercase
        pass

    # should get list of tokens
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
            Token("ASSIGN", "As"),
            Token("ID", "uno"),
            Token("EQ", "="),
            Token("NUMBER", "XI"),
            Token("PLUS", "+"),
            Token("NUMBER", "C"),
            Token("NEWLINE", "\n"),

            Token("ASSIGN", "As"),
            Token("ID", "de"),
            Token("EQ", "="),
            Token("IN", "Anagnosi"),
            Token("NEWLINE", "\n"),

            Token("ASSIGN", "As"),
            Token("ID", "tre"),
            Token("EQ", "="),
            Token("ID", "uno"),
            Token("PLUS", "+"),
            Token("ID", "de"),
            Token("NEWLINE", "\n"),

            Token("OUT", "Grafo"),
            Token("ID", "tre"),
            Token("NEWLINE", "\n")
        ]

        self.assertListEqual(tokens, expected_tokens)
