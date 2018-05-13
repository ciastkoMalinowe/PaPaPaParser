from __future__ import print_function
import entities

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(entities.Variable)
    def printTree(self, indent=0):
        print('| ' * indent + self.value)

    @addToClass(entities.Condition)
    def printTree(self, indent=0):
        print('| ' * indent + 'IF')
        self.bool_expression.printTree(indent+1)
        print('| ' * indent + 'THEN')
        self.statement1.printTree(indent+1)
        if(self.statement2 is not None):
            print('| ' * indent + 'ELSE')
            self.statement2.printTree(indent+1)

    # @addToClass(entities.Constant)
    # def printTree(self, indent=0):
    #     print('| ' * indent + )

    @addToClass(entities.Matrix)
    def printTree(self, indent=0):
        if(self.type == None):
            print('| ' * indent + 'MATRIX')
            self.content.printTree(indent+1)
        else:
            print('| ' * indent + self.type)
            print('| ' * (indent + 1) + self.content)

    @addToClass(entities.Number)
    def printTree(self, indent=0):
        print('| ' * indent + self.type + '(' + self.value + ')')

    @addToClass(entities.BinaryOperation)
    def printTree(self, indent=0):
        print('| ' * indent + self.operator)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(entities.UnaryOperation)
    def printTree(self, indent=0):
        print('| ' * indent + self.operator)
        self.arg.printTree(indent+1)

    @addToClass(entities.Assignment)
    def printTree(self, indent=0):
        print('| ' * indent + self.operator)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(entities.Relation)
    def printTree(self, indent=0):
        print('| ' * indent + self.operator)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(entities.WhileLoop)
    def printTree(self, indent=0):
        print('| ' * indent + 'WHILE')
        self.expr.printTree(indent+1)
        self.prog.printTree(indent+1)

    @addToClass(entities.ForLoop)
    def printTree(self, indent=0):
        print('| ' * indent + 'FOR')
        print('| ' * (indent + 1) + self.id)
        print('| ' * (indent+1) + 'RANGE')
        self.beg.printTree(indent+2)
        self.end.printTree(indent+2)
        self.prog.printTree(indent+1)

    @addToClass(entities.Return)
    def printTree(self, indent=0):
        print('| ' * indent + 'RETURN')

    @addToClass(entities.Break)
    def printTree(self, indent=0):
        print('| ' * indent + 'BREAK')

    @addToClass(entities.Continue)
    def printTree(self, indent=0):
        print('| ' * indent + 'CONTINUE')

    @addToClass(entities.Print)
    def printTree(self, indent=0):
        print('| ' * indent + 'PRINT')
        self.list.printTree(indent+1)

    @addToClass(entities.Index)
    def printTree(self, indent=0):
        print('| ' * indent + 'INDEX')
        print('| ' * (indent + 1) + self.val)

    @addToClass(entities.Program)
    def printTree(self, indent=0):
        self.stat.printTree(indent)
        self.prog.printTree(indent)

    @addToClass(entities.Empty)
    def printTree(self, indent=0):
        pass

    @addToClass(entities.IDAt)
    def printTree(self, indent=0):
        print('| ' * indent + 'REF')
        print('| ' * (indent+1) + self.id)
        self.i1.printTree(indent+1)
        self.i2.printTree(indent+1)


    @addToClass(entities.ID)
    def printTree(self, indent=0):
        print('| ' * indent + self.id)
        # self.id.printTree(indent)


    @addToClass(entities.List)
    def printTree(self, indent=0):
        for val in self.value:
            val.printTree(indent+1)


    @addToClass(entities.List2D)
    def printTree(self, indent=0):
        for val in self.value:
            print('| ' * indent + "VECTOR")
            val.printTree(indent+1)