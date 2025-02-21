NUMBER = 'NUMBER'
IDENTIFIER = 'ID'
NEWLINE = 'NEWLINE'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULT = "MULT"
DIV = 'DIV'
EQ = 'EQ'
LP = 'LP'
RP = 'RP'
ASSIGN = 'ASSIGN'
OUT = 'OUT'
FUNC = 'FUNC'
BRANCH = 'BRANCH'
IN = 'IN'

single_char_tokens = {
    '+': PLUS,
    '-': MINUS,
    '*': MULT,
    '/': DIV,
    '=': EQ,
    '(': LP,
    ')': RP
}

reserved = {
    'As': ASSIGN,
    'Grafo': OUT,
    'Munus': FUNC,
    'Sinon': BRANCH,
    'Anagnosi': IN
}
