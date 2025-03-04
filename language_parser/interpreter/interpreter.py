import copy

from language_parser.syntax_tree.syntax_tree import parse
from language_parser.tokenizer import Tokenizer
from language_parser.tokenizer.consts import NUMBER, IDENTIFIER, FUNC, ASSIGN, OUT, PLUS, MINUS, MULT, DIV, IN


def roman_to_int(roman):
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
                 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for ch in reversed(roman):
        value = roman_map.get(ch, 0)
        if value < prev_value:
            total -= value
        else:
            total += value
            prev_value = value

    return total


class Function:
    def __init__(self, param_names, body):
        self.param_names = param_names
        self.body = body

    def __repr__(self):
        return f"<Function params={self.param_names}>"


class Interpreter:
    def __init__(self):
        # mapping
        self.env = {}

    def interpret(self, ast):
        return self.evaluate(ast)

    def evaluate(self, node):
        """
        Recursively evaluates an AST node.
        """
        if node is None:
            return None

        # --- Statement Level Evaluations ---
        # Process the root node by evaluating each child (statement) sequentially.
        if node.type == "ROOT":  # todo: create note type root as well?
            result = None
            for child in node.children:
                result = self.evaluate(child)

            return result

        # If node is a simple token (a leaf without children)
        if not hasattr(node, 'children'):
            if node.type == NUMBER:
                return roman_to_int(node.value)

            if node.type == IDENTIFIER:
                if node.value in self.env:
                    return self.env[node.value]
                else:
                    # todo: write a test
                    raise ValueError(f"Undefined variable '{node.value}'")

            return node.value

        # Function definition: "Munus ..."
        if node.type == FUNC:
            # node.children[0] is the function name node. Its own children (if any) are the parameters.
            func_name_node = node.children[0]
            func_name = func_name_node.value
            arguments = [child.value for child in func_name_node.children] if func_name_node.children else []
            # The function body is the third child (after  EQ).
            func_body = node.children[2]
            self.env[func_name] = Function(arguments, func_body)

            return None

        # Assignment: "As <identifier> '=' <expression>"
        if node.type == ASSIGN:
            # todo: refactor this branch
            if node.children[2].type == IN:
                var_name_node = node.children[0]
                var_name = var_name_node.value
                # todo: or should it be roman?
                var = input("Enter your INT value here:\n")
                int_var = int(var)

                self.env[var_name] = int_var
                return int_var

            var_name_node = node.children[0]
            var_name = var_name_node.value
            expr = node.children[2]
            result = self.evaluate(expr)
            self.env[var_name] = result

            return result

        # Output: "Grafo ..."
        if node.type == OUT:
            var_name_node = node.children[0]
            var_name = var_name_node.value
            if var_name in self.env:
                result = self.env[var_name]
            else:
                raise ValueError(f"Undefined variable '{var_name}'")

            print(result)
            return result

        # --- Expression Evaluations ---
        # Binary arithmetic operators: PLUS, MINUS, MULT, DIV
        if node.type in (PLUS, MINUS, MULT, DIV):
            left = self.evaluate(node.children[0])
            right = self.evaluate(node.children[1])

            if node.type == PLUS:
                return left + right
            elif node.type == MINUS:
                return left - right
            elif node.type == MULT:
                return left * right
            elif node.type == DIV:
                return left // right if isinstance(left, int) and isinstance(right, int) else left / right

        # Branch operator: simply evaluate its child expression.
        # if node_type == BRANCH:
        #     # fixme: there is a bug currently, in Sinon 1rt arg is treated as function,
        #     #  we should keep the context that it is inside the branch
        #     return self.evaluate(node.children[0], env)

        # Function call:
        # If an IDENTIFIER node has children, we treat it as a function call.
        # todo: check with Sinon n <expr>
        if node.type == IDENTIFIER and node.children:
            func = self.env.get(node.value)
            if func is None:
                raise ValueError(f"Undefined function '{node.value}'")
            if not isinstance(func, Function):
                raise ValueError(f"'{node.value}' is not callable")
            # Evaluate each argument.
            args = [self.evaluate(child) for child in node.children]
            if len(args) != len(func.param_names):
                raise ValueError(f"Function '{node.value}' expects {len(func.param_names)} arguments, got {len(args)}")

            for param, arg in zip(func.param_names, args):
                self.env[param] = arg

            return self.evaluate(func.body)

        # Variable reference: simple identifier with no children.
        if node.type == IDENTIFIER:
            if node.value in self.env:
                return self.env[node.value]
            else:
                raise ValueError(f"Undefined variable '{node.value}'")

        # Number literal.
        if node.type == NUMBER:
            return roman_to_int(node.value)

        return node.value


if __name__ == '__main__':
    code = """
        As uno = XI + C
        As de = Anagnosi
        As tre = uno + de
        Grafo tre
        """

    tokens = Tokenizer.tokenize(code)
    ast_root = parse(tokens)

    interpreter = Interpreter()
    interpreter.interpret(ast_root)
