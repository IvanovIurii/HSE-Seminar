from language_parser.common.consts import (
    NUMBER,
    IDENTIFIER,
    FUNC,
    ASSIGN,
    OUT,
    PLUS,
    MINUS,
    MULT,
    DIV,
    IN,
    romans,
    BRANCH
)


def roman_to_int(roman):
    total = 0
    prev_value = 0
    for ch in reversed(roman):
        value = romans.get(ch, 0)
        if value < prev_value:
            total -= value
        else:
            total += value
            prev_value = value

    return total


def int_to_roman(num):
    if num <= 0:
        return "N"  # Using "N" for zero or negative values.
    values = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    roman = ""
    for value, numeral in values:
        while num >= value:
            roman += numeral
            num -= value

    return roman


class Function:
    def __init__(self, param_names, body):
        self.param_names = param_names
        self.body = body

    def __repr__(self):
        return f"<Function params={self.param_names}>"


class Interpreter:
    def __init__(self):
        self.env = {}

    def interpret(self, ast):
        return int_to_roman(self.evaluate(ast, self.env))

    def evaluate(self, node, env=None):
        if node is None:
            return None

        if env is None:
            env = self.env

        if node.type == "ROOT":
            result = None
            for child in node.children:
                result = self.evaluate(child, env)

            return result

        # If node is a simple term token (a leaf without children)
        if not hasattr(node, 'children') or node.children == []:
            if node.type == NUMBER:
                return roman_to_int(node.value)

            if node.type == IDENTIFIER:
                if node.value in env:
                    return env[node.value]
                else:
                    raise ValueError(f"Undefined variable '{node.value}'")

            return node.value

        # todo: refactor this mess
        # MUNUS
        if node.type == FUNC:
            func_name_node = node.children[0]
            func_name = func_name_node.value
            param_names = [child.value for child in func_name_node.children] if func_name_node.children else []
            func_body = node.children[2]
            env[func_name] = Function(param_names, func_body)

            return None

        # Assignment: "As <identifier> '=' <expression>"
        if node.type == ASSIGN:
            if node.children[2].type == IN:
                var_name_node = node.children[0]
                var_name = var_name_node.value
                var = input("Enter your INT value here:\n")
                int_var = int(var)
                env[var_name] = int_var
                return int_var

            var_name_node = node.children[0]
            var_name = var_name_node.value
            expr = node.children[2]
            result = self.evaluate(expr, env)
            env[var_name] = result

            return result

        # GRAFO
        if node.type == OUT:
            var_name_node = node.children[0]
            var_name = var_name_node.value
            if var_name in env:
                result = env[var_name]
            else:
                raise ValueError(f"Undefined variable '{var_name}'")

            if isinstance(result, Function):
                result = self.evaluate(result.body, env)

            print(result)
            return result

        # Binary arithmetic operators: PLUS, MINUS, MULT, DIV
        if node.type in (PLUS, MINUS, MULT, DIV):
            left = self.evaluate(node.children[0], env)
            right = self.evaluate(node.children[1], env)
            if node.type == PLUS:
                return left + right
            elif node.type == MINUS:
                return left - right
            elif node.type == MULT:
                return left * right
            elif node.type == DIV:
                if isinstance(left, int) and isinstance(right, int):
                    return left // right
                else:
                    return left / right

        if node.type == BRANCH:
            # The branch node has one child (the condition node), whose own children are left and right expressions.
            condition_val = env.get(node.children[0].value)
            if condition_val <= 0:
                return self.evaluate(node.children[0].children[0], env)
            else:
                return self.evaluate(node.children[0].children[1], env)

        # Function call: an IDENTIFIER node with children.
        if node.type == IDENTIFIER and node.children:
            func = env.get(node.value)
            if func is None:
                raise ValueError(f"Undefined function '{node.value}'")
            if not isinstance(func, Function):
                raise ValueError(f"'{node.value}' is not callable")
            args = [self.evaluate(child, env) for child in node.children]
            if len(args) != len(func.param_names):
                raise ValueError(f"Function '{node.value}' expects {len(func.param_names)} arguments, got {len(args)}")

            # Create a new local environment for the function call.
            local_env = dict(env)
            for param, arg in zip(func.param_names, args):
                local_env[param] = arg
            # Ensure that the function itself is available for recursion.
            local_env[node.value] = func
            return self.evaluate(func.body, local_env)

        return node.value
