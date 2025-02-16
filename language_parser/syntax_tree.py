from language_parser.tokenizer.consts import NEWLINE, IDENTIFIER, NUMBER
from language_parser.tokenizer import Tokenizer


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
            child.print_recursively(indent + 1)


def parse_expression(tokens):
    return parse_addition(tokens)


def parse_addition(tokens):
    left = parse_multiplication(tokens)

    while tokens and tokens[0].type in ['PLUS', 'MINUS']:
        bin_op = tokens.pop(0)

        right = parse_multiplication(tokens)

        bin_op.add_child(left)
        bin_op.add_child(right)

        left = bin_op

    return left


def parse_multiplication(tokens):
    left = parse_application(tokens)

    while tokens and tokens[0].type in ['MULT', 'DIV']:
        bin_op = tokens.pop(0)

        right = parse_application(tokens)

        bin_op.add_child(left)
        bin_op.add_child(right)
        left = bin_op

    return left


def parse_application(tokens):  # todo: rename
    node = parse_first(tokens)  # id or number

    # not sure here, but
    # if there is ID or NUMBER after ID without op,
    # most likely we are in a function call
    if tokens and tokens[0].type in [IDENTIFIER, NUMBER]:
        call_node = Node('CALL', node.value)

        while tokens and (tokens[0].type in [IDENTIFIER, NUMBER] or tokens[0].value == '('):
            arg = parse_first(tokens)
            call_node.add_child(arg)

            node = call_node

    return node


def parse_first(tokens):  # todo: rename
    token = tokens.pop(0)
    if token.type in ['ID', 'NUMBER']:
        return token

    if token.type == 'LP':
        expression = parse_expression(tokens)
        tokens.pop(0)  # close RP

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
    if first.type == 'FUNC':
        # minimal function definition is 5 tokens: FUNC <name> <param> EQ <expression>
        if len(tokens) < 5:
            raise ValueError("Invalid function definition")
        func = first
        func_name = tokens[1]
        params = []
        i = 2
        while tokens[i].type != 'EQ':
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

    if first.type == 'ASSIGN':
        # minimal assign definition is 4 tokens: AS <ID> EQ <expression>
        if len(tokens) < 4:
            raise ValueError("Invalid assignment statement: " + " ".join(t.value for t in tokens))  # todo: test this

        first.add_child(tokens[1])  # ID
        first.add_child(tokens[2])  # EQ
        expression = parse_expression(tokens[3:])
        first.add_child(expression)

        return first

    if first.type == 'OUT':
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
