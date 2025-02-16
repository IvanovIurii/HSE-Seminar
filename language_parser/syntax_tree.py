from language_parser.tokenizer.consts import NEWLINE


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
    left_node = tokens.pop(0)

    # todo: better operate with kind, not with its implementation
    while tokens and tokens[0].value in ['+', '-', '*', '/']:
        operator_node = tokens.pop(0)
        right_node = tokens.pop(0)

        operator_node.add_child(left_node)
        operator_node.add_child(right_node)

        left_node = operator_node

    return left_node


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

    # todo: check if this one is needed
    if current_line:
        lines.append(current_line)

    return lines


def parse(tokens):
    root = Node('ROOT', 'root')

    lines = get_lines(tokens)
    for line in lines:
        for idx, _ in enumerate(line):
            node = line[idx]
            if node.type == 'ASSIGN':
                id_node = line[idx + 1]  # ID
                node.add_child(id_node)

                eq_node = line[idx + 2]  # EQ
                node.add_child(eq_node)

                # recursively add the right side
                node.add_child(parse_expression(line[3:]))

                root.add_child(node)

            if node.type == 'OUT':
                id_node = line[idx + 1]  # ID
                node.add_child(id_node)

                root.add_child(node)

            if node.type == 'FUNC':
                id_node = line[idx + 1]  # ID of function

                i = 2
                while line[idx + i].type != "EQ":
                    id_node.add_child(line[idx + i])
                    i += 1

                node.add_child(id_node)

                eq_node = line[idx + i]
                node.add_child(eq_node)

                node.add_child(parse_expression(line[i + 1:]))

                root.add_child(node)

    return root
