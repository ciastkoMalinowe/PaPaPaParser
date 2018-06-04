
class Type:

    def __init__(self, type):
        self.type = type

    def is_id(self):
        return self.type == 'id'

    def is_numeric(self):
        return self.type in ['float', 'int']

    def is_matrix(self):
        return self.type == 'matrix'

    def is_integer(self):
        return self.type == 'int'

    def is_boolean(self):
        return self.type == 'boolean'


class Id(Type):
    def __init__(self):
        Type.__init__(self,'id')


class List(Type):
    def __init__(self, length, element_type):
        Type.__init__(self,'list')
        self.length = length
        self.element_type = element_type


class Matrix(Type):

    def __init__(self, x, y, element_type):
        Type.__init__(self,'matrix')
        self.x = x
        self.y = y
        self.element_type = element_type


class Float(Type):
    def __init__(self):
        Type.__init__(self,'float')


class Int(Type):
    def __init__(self):
        Type.__init__(self,'int')


class Boolean(Type):
    def __init__(self):
        Type.__init__(self,'boolean')