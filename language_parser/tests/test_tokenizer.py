import unittest
from language_parser.tokenizer import Tokenizer
from language_parser.tokenizer.tokenizer import Token


class TestTokenizer(unittest.TestCase):

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
