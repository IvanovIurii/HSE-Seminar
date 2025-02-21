from language_parser.tokenizer.consts import (
    NEWLINE,
    IDENTIFIER,
    NUMBER,
    PLUS,
    MINUS,
    MULT,
    DIV,
    LP,
    RP,
    FUNC,
    EQ,
    ASSIGN,
    OUT,
    BRANCH
)
from language_parser.tokenizer import Tokenizer


# todo: create a class called AST or something

class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.type}: {self.value}"

    def print_recursively(self, indent=0):
        print("  " * indent + str(self))
        for child in self.children:
            if child:
                child.print_recursively(indent + 1)


# <statement>    ::= <func> | <assignment> | <output>
#
# <func>     ::= "Munus" <identifier> { <identifier> } "=" <expression>
# <assignment>   ::= "As" <identifier> "=" <expression>
# <output>       ::= "Grafo" <identifier>
#
# <expression>   ::= <term> { ("+" | "-") <term> }
# <term>         ::= <factor> { ("*" | "/") <factor> }
# <factor>       ::= <primary> { <primary> } // function call
# <primary>      ::= <identifier> | <number> | "(" <expression> ")"
#
# <identifier>   ::= <letter> { <letter> }
# <number>       ::= <roman_numeral>
# <roman_numeral>::= <roman_digit> { <roman_digit> }
# <roman_digit>  ::= "I" | "V" | "X" | "L" | "C" | "D" | "M"
#
# <letter>       ::= "a" | "b" | "c" | ... | "z" // lowercase

# todo: refactor this function and add branch to the grammar
def parse_expression(tokens):
    left = parse_term(tokens)

    while tokens and tokens[0].type in [PLUS, MINUS]:
        bin_op = tokens.pop(0)

        right = parse_term(tokens)

        bin_op.add_child(left)
        bin_op.add_child(right)

        left = bin_op

    return left


def parse_term(tokens):
    left = parse_factor(tokens)

    while tokens and tokens[0].type in [MULT, DIV]:
        bin_op = tokens.pop(0)

        right = parse_factor(tokens)

        bin_op.add_child(left)
        bin_op.add_child(right)
        left = bin_op

    return left


def parse_factor(tokens):
    node = parse_primary(tokens)  # id, number or parenthesis

    # not sure here, but
    # if there is ID or NUMBER, or LP/RP after ID without op,
    # most likely we are in a function call, or it is a (grouped) expression
    if tokens and (tokens[0].type in [IDENTIFIER, NUMBER] or tokens[0].value == '('):
        call_node = Node('CALL', node.value)

        while tokens and (tokens[0].type in [IDENTIFIER, NUMBER] or tokens[0].value == '('):
            arg = parse_primary(tokens)
            call_node.add_child(arg)

            node = call_node

    return node


def parse_primary(tokens):
    if tokens and tokens[0].type == BRANCH:
        branch_token = tokens.pop(0)
        node = parse_expression(tokens)

        branch_token.add_child(node.children[0])  # false
        branch_token.add_child(node.children[1])  # true

        return branch_token

    if tokens:
        token = tokens.pop(0)
        if token.type in [IDENTIFIER, NUMBER]:
            return token

        if token.type == LP:
            expression = parse_expression(tokens)
            closing = tokens.pop(0)
            if closing.type != RP:
                raise ValueError("Missing closing parenthesis")

            return expression

        raise ValueError("Unexpected initial token in the expression: " + str(token))


def get_lines(tokens):
    """
    Splits the token list (from the tokenizer) into a list of lines.
    Each line is a list of Nodes (converted from tokens).
    """
    lines = []
    current_line = []

    for token in tokens:
        if token.key == NEWLINE:
            if current_line:
                lines.append(current_line)
                current_line = []
        else:
            current_line.append(Node(token.key, token.value))

    return lines


def parse_statement(tokens):
    if not tokens:
        return None

    first = tokens[0]
    if first.type == FUNC:
        # minimal function definition is 5 tokens: FUNC <name> <param> EQ <expression>
        if len(tokens) < 5:
            raise ValueError("Invalid function definition")
        func = first
        func_name = tokens[1]
        params = []
        i = 2
        while tokens[i].type != EQ:
            params.append(tokens[i])
            i += 1

        # todo: test broken functional token without EQ, without expression, with invalid param names
        # if i >= len(tokens) or tokens[i].type != 'EQ':
        #     raise ValueError("Missing '=' in function definition")

        eq = tokens[i]
        i += 1
        expression = parse_expression(tokens[i:])
        for p in params:
            func_name.add_child(p)

        func.add_child(func_name)
        func.add_child(eq)
        func.add_child(expression)

        return func

    if first.type == ASSIGN:
        # minimal assign definition is 4 tokens: AS <ID> EQ <expression>
        if len(tokens) < 4:
            raise ValueError("Invalid assignment statement: " + " ".join(t.value for t in tokens))  # todo: test this

        first.add_child(tokens[1])  # ID
        first.add_child(tokens[2])  # EQ
        expression = parse_expression(tokens[3:])
        first.add_child(expression)

        return first

    if first.type == OUT:
        # minimal assign definition: OUT <ID>
        if len(tokens) != 2:
            raise ValueError("Invalid output statement")

        first.add_child(tokens[1])
        return first


def parse(tokens):
    root = Node('ROOT', 'root')
    lines = get_lines(tokens)
    for line in lines:
        stmt = parse_statement(line)
        if stmt:
            root.add_child(stmt)

    return root


if __name__ == '__main__':
    code = """
        Munus sum a b c = a + b + c
        As computo = sum XI C I
        Grafo computo
        """

    tokens = Tokenizer.tokenize(code)
    ast_root = parse(tokens)
    ast_root.print_recursively()

    # todo: introduce comments as %%
