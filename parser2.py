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
        print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, scanner.find_column(p),
                                                                                  p.type, p.value))
    else:
        print("Unexpected end of input")

def p_program(p):
    """program : statement program
                | loop program"""
    p[0] = Program(p)

def p_program_empty(p):
    """program : empty"""
    p[0] = Empty(p)

def p_empty(p):
    """empty :"""


################################################
# ...............statements.....................
################################################

def p_expression_assign(p):
    """statement : id_expression ASSIGN expression ';'
                  | id_expression ASSIGN_ADD expression ';'
                  | id_expression ASSIGN_SUB expression ';'
                  | id_expression ASSIGN_MUL expression ';'
                  | id_expression ASSIGN_DIV expression ';'"""
    p[0] = Assignment(p)

def p_expression_statement(p):
    """statement : expression ';'"""
    p[0] = p[1]

def p_print(p):
    """statement : PRINT list ';'"""
    p[0] = Print(p)

def p_loop_while(p):
    """loop : WHILE '(' bool_expression ')' '{' program '}' """
    p[0] = WhileLoop(p)


def p_loop_for(p):
    """loop : FOR ID ASSIGN index RANGE index '{' program '}'"""
    p[0] = ForLoop(p)

def p_condition_if(p):
    """statement : IF '(' bool_expression ')' statement %prec IFX
                | IF '(' bool_expression ')' statement ELSE statement"""
    p[0] = Condition(p)


def p_break(p):
    """statement : BREAK ';'"""
    p[0] = Break(p)

def p_continue(p):
    """statement : CONTINUE ';'"""
    p[0] = Continue(p)

def p_return(p):
    """statement : RETURN ';'"""
    p[0] = Return(p)

################################################
# ...............expressions....................
################################################

def p_expression(p):
    """expression : '(' expression ')'
                | bool_expression
                | num_expression
                | matrix_expression
                | id_expression
                | STRING"""

    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_expression_id(p):
    """id_expression : ID '[' index ',' index  ']'
                | ID """
    if(len(p) > 2):
        p[0] = IDAt(p)
    else:
        p[0] = ID(p)


################################################
# ..........numerical expressions...............
################################################

def p_num_expression_add(p):
    """num_expression : num_expression ADD num_expression
                    | id_expression ADD id_expression
                    | num_expression ADD id_expression
                    | id_expression ADD num_expression"""
    p[0] = BinaryOperation(p, 'num', '+')

def p_num_expression_sub(p):
    """num_expression : num_expression SUB num_expression
                    | id_expression SUB id_expression
                    | id_expression SUB num_expression
                    | num_expression SUB id_expression"""
    p[0] = BinaryOperation(p, 'num', '-')

def p_num_expression_div(p):
    """num_expression : num_expression DIV num_expression
                    | id_expression DIV id_expression
                    | id_expression DIV num_expression
                    | num_expression DIV id_expression"""
    p[0] = BinaryOperation(p, 'num', '/')

def p_num_expression_mul(p):
    """num_expression : num_expression MUL num_expression
                    | id_expression MUL id_expression
                    | num_expression MUL id_expression
                    | id_expression MUL num_expression"""
    p[0] = BinaryOperation(p, 'num', '*')

def p_num_expression_unary_minus(p):
    """num_expression : SUB num_expression %prec U_SUB
                    | SUB id_expression %prec U_SUB"""
    p[0] = UnaryOperation(p, p[1])

def p_num_expression_int(p):
    """num_expression : INT_NUM"""
    p[0] = Number(p,'int')

def p_num_expression_float(p):
    """num_expression : FLOAT_NUM"""
    p[0] = Number(p, 'float')

'''
def p_num_expression_id(p):
    """num_expression : id_expression"""
    p[0] = Number(p[0])
'''
def p_index(p):
    """index : ID
        | INT_NUM"""
    p[0] = Index(p)

################################################
# ..........matrix expressions..................
################################################

def p_matrix_expression_init(p):
    """matrix_expression : ZEROS '(' INT_NUM ')'
                 | ONES '(' INT_NUM ')'
                 | EYE '(' INT_NUM ')'"""

    p[0] = Matrix(p, type=p[1])

def p_matrix_expression_value(p):
    """matrix_expression :  '[' ']'
                 | '[' lists ']'"""
    p[0] = Matrix(p)

'''
def p_matrix_expression_id(p):
    """matrix_expression :  id_expression"""
    p[0] = Matrix(p)
'''
def p_matrix_expression_transpose(p):
    """matrix_expression : matrix_expression TRANSPOSE
                        | id_expression TRANSPOSE"""
    p[0] = UnaryOperation(p, p[2])


def p_matrix_expression_add(p):
    """matrix_expression : matrix_expression DOT_ADD matrix_expression
                | id_expression DOT_ADD id_expression
                | matrix_expression DOT_ADD id_expression
                | id_expression DOT_ADD matrix_expression"""

    p[0] = BinaryOperation(p, 'matrix', '+')

def p_matrix_expression_sub(p):
    """matrix_expression : matrix_expression DOT_SUB matrix_expression
                | id_expression DOT_SUB id_expression
                | id_expression DOT_SUB matrix_expression
                | matrix_expression DOT_SUB id_expression"""

    p[0] = BinaryOperation(p, 'matrix', '-')

def p_matrix_expression_mul(p):
    """matrix_expression : matrix_expression DOT_MUL matrix_expression
                | id_expression DOT_MUL id_expression
                | id_expression DOT_MUL matrix_expression
                | matrix_expression DOT_MUL id_expression"""

    p[0] = BinaryOperation(p, 'matrix', '*')

def p_matrix_expression_div(p):
    """matrix_expression : matrix_expression DOT_DIV matrix_expression
                | id_expression DOT_DIV id_expression
                | id_expression DOT_DIV matrix_expression
                | matrix_expression DOT_DIV id_expression"""

    p[0] = BinaryOperation(p, 'matrix', '/')

def p_matrix_expression_unary_minus(p):
    """matrix_expression : DOT_SUB matrix_expression %prec U_DOT_SUB
                        | DOT_SUB id_expression %prec U_DOT_SUB"""
    p[0] = UnaryOperation(p, p[1])

################################################
# ..........lists ..............................
################################################

def p_lists(p):
    """lists : vector ';' lists
            | vector"""
    if len(p) > 3:
        p[0] = List2D(p[1])
        p[0].append(p[3])
    else:
        p[0] = List2D(p[1])

def p_num__list(p):
    """vector : num_expression ',' list
            | num_expression"""
    if len(p) > 3:
        p[0] = Vector(p[1])
        p[0].extend(p[3])
    else:
        p[0] = Vector(p[1])

def p_list(p):
    """list : expression ',' list
            | expression"""
    if len(p) > 3:
        p[0] = List(p[1])
        p[0].extend(p[3])
    else:
        p[0] = List(p[1])

################################################
# ..........bool expressions....................
################################################

def p_num_expression_rel(p):
    """bool_expression : num_expression LESS num_expression
                | id_expression LESS id_expression
                | num_expression LESS id_expression
                | id_expression LESS num_expression
                | num_expression LESS_OR_EQ num_expression
                | id_expression LESS_OR_EQ id_expression
                | id_expression LESS_OR_EQ num_expression
                | num_expression LESS_OR_EQ id_expression
                | num_expression GREATER num_expression
                | id_expression GREATER id_expression
                | id_expression GREATER num_expression
                | num_expression GREATER id_expression
                | num_expression GREATER_OR_EQ num_expression
                | id_expression GREATER_OR_EQ id_expression
                | id_expression GREATER_OR_EQ num_expression
                | num_expression GREATER_OR_EQ id_expression
                | num_expression EQ num_expression
                | id_expression EQ id_expression
                | id_expression EQ num_expression
                | num_expression EQ id_expression
                | num_expression NOT_EQ num_expression
                | id_expression NOT_EQ id_expression
                | id_expression NOT_EQ num_expression
                | num_expression NOT_EQ id_expression"""
    p[0] = Relation(p)


parser = yacc.yacc()
