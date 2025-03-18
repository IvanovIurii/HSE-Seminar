from language_parser.syntax_tree.mermaid import save_mermaid_to_markdown
from language_parser.common.consts import (
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
    BRANCH,
    IN
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

    def to_mermaid_markdown(self, name):
        save_mermaid_to_markdown(self, name)


# <statement>    ::= <func> | <assignment> | <output>
#
# <func>     ::= "Munus" <identifier> { <identifier> } "=" <expression>
# <assignment>   ::= "As" <identifier> "=" <expression>
# <output>       ::= "Grafo" <identifier>
#
# <expression>   ::= <term> { ("+" | "-") <term> }
# <term>         ::= <factor> { ("*" | "/") <factor> }
# <factor>       ::= <primary> { <primary> } // function call
# <primary>      ::= <identifier> | <number> | <input> | "(" <expression> ")" | branch <expression>
#
# <identifier>   ::= <letter> { <letter> }
# <number>       ::= <roman_numeral>
# <roman_numeral>::= <roman_digit> { <roman_digit> }
# <roman_digit>  ::= "I" | "V" | "X" | "L" | "C" | "D" | "M"
#
# <letter>       ::= "a" | "b" | "c" | ... | "z" // lowercase

# todo: refactor this function
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
    node = parse_primary(tokens)  # id, number, input, ternary operator or parenthesis

    while tokens and (tokens[0].type in [IDENTIFIER, NUMBER] or tokens[0].value == '('):
        arg = parse_primary(tokens)
        node.add_child(arg)

    return node


def parse_primary(tokens):
    if tokens and tokens[0].type == BRANCH:
        branch_token = tokens.pop(0)
        condition_expression = parse_expression(tokens)
        #  todo: maybe new type
        branch_token.add_child(condition_expression)

        return branch_token

    if tokens:
        token = tokens.pop(0)

        if token.type in [IDENTIFIER, NUMBER, IN]:
            return token

        if token.type == LP:
            expression = parse_expression(tokens)
            if not tokens:
                raise ValueError("Missing closing parenthesis")

            closing = tokens.pop(0)
            if closing.type != RP:
                raise ValueError("Missing closing parenthesis")

            return expression

        raise ValueError("Unexpected initial token in the expression: " + str(token))


def get_lines(tokens):
    """
    Splits the token list (from the tokenizer) into a list of lines by NEWLINE token.
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

    if current_line:
        lines.append(current_line)

    return lines


def parse_statement(tokens):
    if not tokens:
        return None

    first = tokens[0]
    if first.type == FUNC:
        # minimal function definition is 5 tokens: FUNC <name> EQ <expression>
        if len(tokens) < 4:
            raise ValueError("Invalid function definition")
        func = first
        func_name = tokens[1]
        params = []
        i = 2
        while tokens[i].type != EQ:
            params.append(tokens[i])
            i += 1

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
            raise ValueError("Invalid output statement")  # todo: test this

        first.add_child(tokens[1])
        return first

    raise ValueError("Invalid start")


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
        As uno = XI + C
        As de = Anagnosi
        """

    tokens = Tokenizer.tokenize(code)
    ast_root = parse(tokens)

    ast_root.print_recursively()
