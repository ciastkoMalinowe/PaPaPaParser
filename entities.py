class ID:
    def __init__(self, p, line):
        self.line = line
        self.id = p[1]


class IDAt:
    def __init__(self, p, line):
        self.line = line
        self.id = p[1]
        self.index1 = p[3]
        self.index2 = p[5]


class Condition:
    def __init__(self, p, line):
        self.line = line
        self.bool_expression = p[3]
        self.statement1 = p[5]
        self.statement2 = None
        if len(p) > 6:
            self.statement2 = p[7]


class Matrix:

    def __init__(self, p, line, type=None):
        self.line = line
        self.type = type
        if type is None:
            self.content = p[2]
            self.x = len(p[2].get_value())
            if self.x != 0:
                self.y = len(p[2].get_value()[0].get_value())
            else:
                self.y = 0
        else:
            self.content = p[3]
            self.x = p[3]
            self.y = p[3]


class Number:

    def __init__(self, p, line, type):
        self.line = line
        self.value = p[1]
        self.type = type


class BinaryOperation:

    def __init__(self, p, line):
        self.line = line
        self.operator = p[2]
        self.left = p[1]
        self.right = p[3]


class UnaryOperation:

    def __init__(self, p, line, operator):
        self.line = line
        self.operator = operator
        if self.operator == '\'':
            self.arg = p[1]
        else:
            self.arg = p[2]

class Assignment:

    def __init__(self, p, line):
        self.line = line
        self.left = p[1]
        self.operator = p[2]
        self.right = p[3]

class Relation:

    def __init__(self, p, line):
        self.line = line
        self.left = p[1]
        self.operator = p[2]
        self.right = p[3]

class WhileLoop:

    def __init__(self, p, line):
        self.line = line
        self.expr = p[3]
        self.prog = p[6]


class ForLoop:

    def __init__(self, p, line):
        self.line = line
        self.id = p[2]
        self.beg = p[4]
        self.end = p[6]
        self.prog = p[8]

class Return:

    def __init__(self, p, line):
        self.line = line
        self.variable = None
        if(len(p) > 3):
            self.variable = p[2]

class Break:

    def __init__(self, p, line):
        self.line = line


class Continue:

    def __init__(self, p, line):
        self.line = line


class Print:

    def __init__(self, p, line):
        self.line = line
        self.list = p[2]


class Empty:
    def __init__(self, p, line):
        self.line = line


class Program:

    def __init__(self, p, line):
        self.line = line
        self.statement = p[1]
        self.program = p[2]


class List:

    def __init__(self, initial_val, line):
        self.line = line
        self.value = [initial_val]

    def get_value(self):
        return self.value

    def extend(self, lista):
        self.value.extend(lista.get_value())


class List2D:
    def __init__(self, initial_val, line):
        self.line = line
        self.value = [initial_val]

    def get_value(self):
        return self.value

    def append(self, lista):
        self.value.extend(lista.get_value())