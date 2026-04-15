from tockenizer import (
    RR_INT, RR_FLOAT, RR_PLUS, RR_MINUS,
    RR_MULTIPLY, RR_DIVIDE,
    RR_LEFT_PAREN, RR_RIGHT_PAREN, RR_SPACE
)

# ---------------- AST NODES ----------------

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Number({self.value})"


class BiOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op.type} {self.right})"


class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

    def __repr__(self):
        return f"({self.op.type}{self.node})"


# ---------------- PARSER ----------------

class Parser:
    def __init__(self, tokens):
        # Remove whitespace tokens before parsing
        self.tokens = [t for t in tokens if t.type != RR_SPACE]
        self.pos = 0
        self.current_token = None
        self.advance()

    # Move to the next token
    def advance(self):
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None

    # Parse factors: numbers, parentheses, unary operators
    def factor(self):
        token = self.current_token

        # Unary + or -
        if token and token.type in (RR_PLUS, RR_MINUS):
            self.advance()
            return UnaryOpNode(token, self.factor())

        # Parenthesized expression
        if token and token.type == RR_LEFT_PAREN:
            self.advance()
            expr = self.expression()

            if self.current_token and self.current_token.type == RR_RIGHT_PAREN:
                self.advance()
                return expr
            else:
                raise Exception("Unmatched parentheses: missing ')'")

        # Number (int or float)
        if token and token.type in (RR_INT, RR_FLOAT):
            self.advance()
            return NumberNode(token)

        raise Exception(
            f"Unexpected token {token.type if token else 'EOF'} (missing operand)"
        )

    # Handle multiplication and division
    def term(self):
        left = self.factor()

        while self.current_token and self.current_token.type in (RR_MULTIPLY, RR_DIVIDE):
            op_token = self.current_token
            self.advance()
            right = self.factor()
            left = BiOpNode(left, op_token, right)

        return left

    # Handle addition and subtraction
    def expression(self):
        left = self.term()

        while self.current_token and self.current_token.type in (RR_PLUS, RR_MINUS):
            op_token = self.current_token
            self.advance()
            right = self.term()
            left = BiOpNode(left, op_token, right)

        return left


# ---------------- AST PRINTING ----------------

def print_ast(node, indent=""):
    if isinstance(node, NumberNode):
        print(f"{indent}Number({node.value})")

    elif isinstance(node, UnaryOpNode):
        print(f"{indent}UnaryOp({node.op.value})")
        print_ast(node.node, indent + "  ")

    elif isinstance(node, BiOpNode):
        print(f"{indent}BiOp({node.op.value})")
        print_ast(node.left, indent + "  ")
        print_ast(node.right, indent + "  ")