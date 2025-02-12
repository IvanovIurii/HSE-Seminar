class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.type}: {self.value}"

    def print_recursively(self, node):
        print(node)
        for child in self.children:
            self.print_recursively(child)


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
    lines = []
    line = []

    for token in tokens:
        if token.key == 'NEWLINE':
            lines.append(line)
            line = []
        else:
            line.append(Node(token.key, token.value))

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

            # todo: add IN statement

    return root
