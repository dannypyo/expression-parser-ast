## Expression Parser & Lexer (Python)
A simple expression parser and tokenizer built in Python that converts mathematical input into an Abstract Syntax Tree (AST).

This project demonstrates core concepts from compiler design, including:

- Lexical analysis (tokenizing input)
- Parsing expressions
- Building and visualizing an AST

# Description
This program takes user input (mathematical expressions) and processes it in two stages:

1. Lexer (Tokenizer) → Breaks input into tokens
2. Parser → Builds an Abstract Syntax Tree (AST)

The system supports basic arithmetic expressions and prints the resulting AST in a readable format.

# Features
- Tokenizes user input into meaningful symbols
- Supports:
  - Integers & floats
  - Addition (+)
  - Subtraction (-)
  - Multiplication (*)
  - Division (/)
  - Parentheses ()
- Handles:
  - Unary operations (e.g., -6)
  - Nested expressions
- Detects syntax errors
- Displays structured AST output
