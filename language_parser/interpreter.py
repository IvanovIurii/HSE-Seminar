class Interpreter:
    def __init__(self):
        self.variables = {}

    def evaluate(self, node):
        if node.type == 'NUMBER':
            if node.value == 'XI':
                return 11

            return roman_to_integer.get(node.value)

        elif node.type == 'ID':
            return self.variables.get(node.value, 0)

        elif node.type == 'PLUS':
            left_value = self.evaluate(node.children[0])
            right_value = self.evaluate(node.children[1])
            return left_value + right_value

        elif node.type == 'MINUS':
            left_value = self.evaluate(node.children[0])
            right_value = self.evaluate(node.children[1])
            return left_value - right_value

        elif node.type == 'ASSIGN':
            value = self.evaluate(node.children[2])
            self.variables[node.children[0].value] = value
            return value

        # todo: add user input from Terminal
        elif node.type == 'IN':
            return 42

        elif node.type == 'OUT':
            return self.evaluate(node.children[0])

        return 0


# todo: write a function to convert Roman numbers to integers
roman_to_integer = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}
