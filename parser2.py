import scanner
import ply.yacc as yacc
from entities import *
tokens = scanner.tokens

precedence = (
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'ASSIGN', 'ASSIGN_ADD', 'ASSIGN_SUB', 'ASSIGN_MUL', 'ASSIGN_DIV'),
    ('nonassoc', 'GREATER', 'LESS'),  # Nonassociative operators
    ('nonassoc', 'GREATER_OR_EQ', 'LESS_OR_EQ', 'NOT_EQ', 'EQ'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'U_SUB'),  # Unary minus operator
    ('left', 'DOT_ADD', 'DOT_SUB'),
    ('left', 'DOT_MUL', 'DOT_DIV'),
    ('right', 'U_DOT_SUB'),  # Unary minus operator
    ("right", "TRANSPOSE")
)

start = 'program'

def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")

def p_program(p):
    """program : statement program
                | loop program"""
    p[0] = Program(p, p.lexer.lineno - 1)

def p_program_empty(p):
    """program : empty"""
    p[0] = Empty(p, p.lexer.lineno - 1)

def p_empty(p):
    """empty :"""


################################################
# ...............statements.....................
################################################

def p_expression_assign(p):
    """statement : expression ASSIGN expression ';'
                  | expression ASSIGN_ADD expression ';'
                  | expression ASSIGN_SUB expression ';'
                  | expression ASSIGN_MUL expression ';'
                  | expression ASSIGN_DIV expression ';'"""
    p[0] = Assignment(p, p.lexer.lineno - 1)

def p_expression_statement(p):
    """statement : expression ';'"""
    p[0] = p[1]

def p_print(p):
    """statement : PRINT list ';'"""
    p[0] = Print(p, p.lexer.lineno -1)

def p_loop_while(p):
    """loop : WHILE '(' expression ')' '{' program '}' """
    p[0] = WhileLoop(p, p.lexer.lineno -1)


def p_loop_for(p):
    """loop : FOR ID ASSIGN expression RANGE expression '{' program '}'"""
    p[0] = ForLoop(p, p.lexer.lineno -1)

def p_condition_if(p):
    """statement : IF '(' expression ')' statement %prec IFX
                | IF '(' expression ')' statement ELSE statement"""
    p[0] = Condition(p, p.lexer.lineno -1)


def p_break(p):
    """statement : BREAK ';'"""
    p[0] = Break(p, p.lexer.lineno - 1)

def p_continue(p):
    """statement : CONTINUE ';'"""
    p[0] = Continue(p, p.lexer.lineno - 1)

def p_return(p):
    """statement : RETURN expression ';'
                | RETURN ';'"""
    p[0] = Return(p, p.lexer.lineno - 1)

################################################
# ...............expressions....................
################################################

def p_expression(p):
    """expression : '(' expression ')'
                | STRING"""

    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_expression_id(p):
    """expression : ID '[' expression ',' expression  ']'
                | ID """
    if(len(p) > 2):
        p[0] = IDAt(p, p.lexer.lineno - 1)
    else:
        p[0] = ID(p, p.lexer.lineno - 1)


################################################
# ..........numerical expressions...............
################################################

def p_num_expression_add(p):
    """expression : expression ADD expression"""
    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_num_expression_sub(p):
    """expression : expression SUB expression"""
    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_num_expression_div(p):
    """expression : expression DIV expression"""
    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_num_expression_mul(p):
    """expression : expression MUL expression"""
    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_num_expression_unary_minus(p):
    """expression : SUB expression %prec U_SUB"""
    p[0] = UnaryOperation(p, p.lexer.lineno - 1, p[1])

def p_num_expression_int(p):
    """expression : INT_NUM"""
    p[0] = Number(p, p.lexer.lineno - 1, 'int')

def p_num_expression_float(p):
    """expression : FLOAT_NUM"""
    p[0] = Number(p, p.lexer.lineno - 1, 'float')

################################################
# ..........matrix expressions..................
################################################


def p_matrix_expression_init(p):
    """expression : ZEROS '(' INT_NUM ')'
                 | ONES '(' INT_NUM ')'
                 | EYE '(' INT_NUM ')'"""

    p[0] = Matrix(p, p.lexer.lineno - 1, type=p[1])


def p_matrix_expression_value(p):
    """expression :  '[' ']'
                 | '[' list2D ']'"""
    p[0] = Matrix(p, p.lexer.lineno - 1)

def p_matrix_expressions(p):
    """expression : expression TRANSPOSE"""
    p[0] = UnaryOperation(p, p.lexer.lineno - 1, p[2])

def p_matrix_expression_add(p):
    """expression : expression DOT_ADD expression"""

    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_matrix_expression_sub(p):
    """expression : expression DOT_SUB expression"""

    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_matrix_expression_mul(p):
    """expression : expression DOT_MUL expression"""

    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_matrix_expression_div(p):
    """expression : expression DOT_DIV expression"""

    p[0] = BinaryOperation(p, p.lexer.lineno - 1)

def p_matrix_expression_unary_minus(p):
    """expression : DOT_SUB expression %prec U_DOT_SUB"""
    p[0] = UnaryOperation(p, p.lexer.lineno - 1, p[1])

################################################
# ....................list......................
################################################


def p_list2D(p):
    """list2D : list ';' list2D
            | list"""
    if len(p) > 3:
        p[0] = List2D(p[1], p.lexer.lineno - 1)
        p[0].append(p[3])
    else:
        p[0] = List2D(p[1], p.lexer.lineno - 1)


def p_list(p):
    """list : expression ',' list
            | expression"""
    if len(p) > 3:
        p[0] = List(p[1], p.lexer.lineno - 1)
        p[0].extend(p[3])
    else:
        p[0] = List(p[1], p.lexer.lineno - 1)

################################################
# .................relations....................
################################################


def p_expression_relation(p):
    """expression : expression LESS expression
                | expression LESS_OR_EQ expression
                | expression GREATER expression
                | expression GREATER_OR_EQ expression
                | expression EQ expression
                | expression NOT_EQ expression"""
    p[0] = Relation(p, p.lexer.lineno - 1)


parser = yacc.yacc()
