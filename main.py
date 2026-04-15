from tockenizer import Lexer
from parser import Parser, print_ast

def run_program(text):
    lexer = Lexer('<stdin>', text)
    tokens = lexer.make_tokens()
    
    print(f"Tokens: {tokens}")

    try:
        parser = Parser(tokens)
        ast = parser.expression()
        
        print("\nAbstract Syntax Tree:")
        print_ast(ast)
    except Exception as e:
        print(f"Syntax Error: {e}")

if __name__ == "__main__":
    while True:
        text = input('R@R > ')
        if text.strip().lower() == 'exit': break
        run_program(text)

# Test Cases
# 3.14+2
# 2*(3+4)
# -6*3
# (5+2
# 10+*5