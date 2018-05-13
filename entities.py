class Variable:

    def __init__(self, p):
        self.p = p
        self.val = p[1]

    def value(self):
        if 1:
            return Matrix([])
        else:
            return Number([])

class ID:
    def __init__(self, p):
        self.p = p
        self.id = p[1]

class IDAt:
    def __init__(self, p):
        self.p = p
        self.id = p[1]
        self.i1 = p[3]
        self.i2 = p[5]

class Condition:
    def __init__(self, p):
        self.p = p
        self.bool_expression = p[3]
        self.statement1 = p[5]
        if len(p) > 6:
            self.statement2 = p[7]


class Constant:

    def __init__(self, p, type):
        self.p = p

class Matrix:

    def __init__(self, p, type=None):
        self.p = p
        self.type = type
        if type is not None:
            self.content = p[3]
        else:
            self.content = p[2]

    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __truediv__(self, other):
        pass

    def transpose(self):
        pass

class Number:

    def __init__(self, p, type):
        self.p = p
        self.value = p[1]
        self.type = type

    def __add__(self, other):
        pass
    def __sub__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __truediv__(self, other):
        pass

class BinaryOperation:

    def __init__(self, p, type, operation_as_string):
        self.p = p
        self.operator = operation_as_string
        self.left = p[1]
        self.right = p[3]

class UnaryOperation:

    def __init__(self, p, operator):
        self.p = p
        self.operator = operator
        if self.operator == '\'':
            self.arg = p[1]
        else:
            self.arg = p[2]

class Assignment:

    def __init__(self, p):
        self.p = p
        self.left = p[1]
        self.operator = p[2]
        self.right = p[3]

class Relation:

    def __init__(self, p):
        self.p = p
        self.left = p[1]
        self.operator = p[2]
        self.right = p[3]

class WhileLoop:

    def __init__(self, p):
        self.p = p
        self.expr = p[3]
        self.prog = p[6]


class ForLoop:

    def __init__(self, p):
        self.p = p
        self.id = p[2]
        self.beg = p[4]
        self.end = p[6]
        self.prog = p[8]

class Return:

    def __init__(self, p):
        self.p = p

class Break:

    def __init__(self, p):
        self.p = p


class Continue:

    def __init__(self, p):
        self.p = p


class Print:

    def __init__(self, p):
        self.p = p
        self.list = p[2]

class Index:

    def __init__(self, p):
        self.p = p
        self.val = p[1]

class Empty:
    def __init__(self, p):
        self.p = p

class Program:

    def __init__(self, p):
        self.p = p
        self.stat = p[1]
        self.prog = p[2]


class List:

    def __init__(self, initial_val):
        self.value = [initial_val]

    def get_value(self):
        return self.value

    def extend(self, lista):
        self.value.extend(lista.get_value())


class List2D:
    def __init__(self, initial_val):
        self.value = [initial_val]

    def get_value(self):
        return self.value

    def append(self, lista):
        self.value.extend(lista.get_value())