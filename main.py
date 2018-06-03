"""import sys
import ply.lex as lex
import scanner


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner.lexer
    lexer.input(text) # Give the lexer some input

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break    # No more input
        column = scanner.find_column(text,tok)
        print("(%d,%d): %s(%s)" %(tok.lineno, column, tok.type, tok.value))
"""

"""
import sys
import scanner
import parser2
from treePrinter import TreePrinter
import ply.yacc as yacc

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner.lexer

    parser = yacc.yacc(module=parser2)
    ast = parser.parse(text, lexer=lexer)
    print (ast)
    ast.printTree()
"""

import sys
import scanner
import parser2
from treePrinter import TreePrinter
from typeChecker import TypeChecker
import ply.yacc as yacc
from Interpreter import Interpreter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = scanner.lexer

    parser = yacc.yacc(module=parser2)
    ast = parser.parse(text, lexer=lexer)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)

    if typeChecker.errors:
        sys.exit(1)
    else:
        interpreter = Interpreter()
        interpreter.visit(ast)