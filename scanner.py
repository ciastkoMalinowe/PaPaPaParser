import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = ['STRING',
          'FLOAT_NUM', 'INT_NUM',
          'DOT_ADD', 'DOT_SUB', 'DOT_MUL', 'DOT_DIV',
          'ASSIGN_ADD', 'ASSIGN_SUB', 'ASSIGN_MUL', 'ASSIGN_DIV',
          'ADD', 'SUB', 'MUL', 'DIV',
          'GREATER_OR_EQ', 'LESS_OR_EQ', 'NOT_EQ', 'EQ',
          'GREATER', 'LESS', 'ASSIGN',
          'TRANSPOSE', 'RANGE',
          'ID'] + list(reserved.values())

literals = ['(', ')', '[', ']', '{', '}', ',', ';']

t_STRING = r'\".*\"'
t_FLOAT_NUM = r'\d+\.\d+'
t_INT_NUM = r'\d+'

t_DOT_ADD = r'\.\+'
t_DOT_SUB = r'\.-'
t_DOT_MUL = r'\.\*'
t_DOT_DIV = r'\./'

t_ASSIGN_ADD = r'\+='
t_ASSIGN_SUB = r'-='
t_ASSIGN_MUL = r'\*='
t_ASSIGN_DIV = r'/='

t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'

t_GREATER_OR_EQ = r'>='
t_LESS_OR_EQ = r'<='
t_NOT_EQ = r'!='
t_EQ = r'=='

t_GREATER = r'>'
t_LESS = r'<'
t_ASSIGN = r'='

t_TRANSPOSE = r'\''
t_RANGE = r'\:'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


t_ignore = '  \t'
t_ignore_COMMENT = r'\#.*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t) :
    print( "Illegal character '%s'" %t.value[0] )
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

lexer = lex.lex()