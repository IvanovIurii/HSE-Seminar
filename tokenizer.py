import re

# maybe saving this in map would be better
# + enums

left_values = [
    ('ASSIGN', r'As'),
    ('OUT', r'Grafo'),
    ('FUNC', r'Munus'),  # define function
    ('BRANCH', r'Sinon'),  # define branch
]

tokens = left_values + [
    ('NUMBER', r'[IVXLCDM]+'),  # integers
    ('IN', r'Anagnosi'),
    ('ID', r'[a-z]+'),  # variables
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULT', r'\*'),
    ('DIV', r'/'),
    ('LP', r'\('),  # left parenthesis
    ('RP', r'\)'),  # right parenthesis
    ('EQ', r'='),
    ('COMMA', r','),
    ('SPACE', r'\s+')
]

regex = '|'.join(f'(?P<{left}>{right})' for left, right in tokens)


class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"{self.kind}: {self.value}"


def tokenize(code):
    for mo in re.finditer(regex, code):
        kind = mo.lastgroup
        value = mo.group()

        # ignore whitespaces
        if kind == 'SPACE':
            continue

        yield Token(kind, value)
