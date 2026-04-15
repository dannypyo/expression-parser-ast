# ---------------- TOKEN CLASS ----------------
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"


# ---------------- TOKEN TYPES ----------------
RR_INT = 'RR_INT'
RR_FLOAT = 'RR_FLOAT'
RR_PLUS = 'RR_PLUS'
RR_MINUS = 'RR_MINUS'
RR_MULTIPLY = 'RR_MULTIPLY'
RR_DIVIDE = 'RR_DIVIDE'
RR_SPACE = 'RR_SPACE'
RR_LEFT_PAREN = 'RR_LEFT_PAREN'
RR_RIGHT_PAREN = 'RR_RIGHT_PAREN'

# Digits and comment character
DIGITS = '0123456789'
COMMENT_CHAR = '#'


# ---------------- POSITION TRACKING ----------------
class Position:
    def __init__(self, idx, ln, col):
        self.idx = idx
        self.ln = ln
        self.col = col

    def copy(self):
        return Position(self.idx, self.ln, self.col)

    def __repr__(self):
        return f"({self.idx}, {self.ln}, {self.col})"


# ---------------- LEXER ----------------
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(0, 1, 0)
        self.current_char = None
        self.advance()

    # Move to the next character in the input
    def advance(self):
        self.pos.idx += 1
        self.pos.col += 1

        if self.pos.idx - 1 < len(self.text):
            self.current_char = self.text[self.pos.idx - 1]
        else:
            self.current_char = None

        # Handle new line tracking
        if self.current_char == '\n':
            self.pos.ln += 1
            self.pos.col = 0

    # Convert input text into a list of tokens
    def make_tokens(self):
        tokens = []

        while self.current_char is not None:

            if self.current_char == '+':
                tokens.append(Token(RR_PLUS, '+'))

            elif self.current_char == '-':
                tokens.append(Token(RR_MINUS, '-'))

            elif self.current_char == '*':
                tokens.append(Token(RR_MULTIPLY, '*'))

            elif self.current_char == '/':
                tokens.append(Token(RR_DIVIDE, '/'))

            elif self.current_char == '(':
                tokens.append(Token(RR_LEFT_PAREN, '('))

            elif self.current_char == ')':
                tokens.append(Token(RR_RIGHT_PAREN, ')'))

            # Skip whitespace
            elif self.current_char == ' ':
                tokens.append(Token(RR_SPACE, ' '))

            # Ignore comments
            elif self.current_char == COMMENT_CHAR:
                self.advance()
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()

            # Build numbers (int or float)
            elif self.current_char in DIGITS + '.':
                tokens.append(self.make_number())

            # Handle unknown characters
            else:
                pos = self.pos.copy()
                print(f"Illegal character '{self.current_char}'")
                print(f"Index: {pos.idx}, Line: {pos.ln}, Column: {pos.col}")
                self.advance()

            self.advance()

        return tokens

    # Convert a sequence of digits into a number token
    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return Token(RR_INT, int(num_str))
        else:
            return Token(RR_FLOAT, float(num_str))


# ---------------- RUN FUNCTION ----------------
def run(fn, text):
    lexer = Lexer(fn, text)
    return lexer.make_tokens()