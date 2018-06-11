import symbol_table
import entities
from memory import *
from Exceptions import *
from visit import *
import copy
import sys

sys.setrecursionlimit(10000)

operations = {
    "+": (lambda l, r: l + r),
    "-": (lambda l, r: l - r),
    "/": (lambda l, r: l / r),
    "*": (lambda l, r: l * r),
    "-u": (lambda e: -e),
    ".+": (lambda l, r: matrix_opertion(l, r, "+")),
    ".-": (lambda l, r: matrix_opertion(l, r, "-")),
    "./": (lambda l, r: matrix_opertion(l, r, "/")),
    ".*": (lambda l, r: matrix_opertion(l, r, "*")),
    ".+=": (lambda l, r: matrix_opertion(l, r, "+")),
    ".-=": (lambda l, r: matrix_opertion(l, r, "-")),
    "./=": (lambda l, r: matrix_opertion(l, r, "/")),
    ".*=": (lambda l, r: matrix_opertion(l, r, "*")),
    "'": (lambda m: transpose(m)),
    "=": (lambda l, r: r),
    "+=": (lambda l, r: l + r),
    "-=": (lambda l, r: l - r),
    "*=": (lambda l, r: l * r),
    "/=": (lambda l, r: l / r),
    "==": (lambda l, r: l == r),
    ">": (lambda l, r: l > r),
    ">=": (lambda l, r: l >= r),
    "<": (lambda l, r: l < r),
    "<=": (lambda l, r: l <= r)
}


def transpose(m):
    return [list(i) for i in zip(*m)]


def matrix_opertion(x, y, op):
    # return [[operations[op](a, b) for a, b in zip(x, y)] for x, y in zip(x, y)]
    r = copy.copy(x)
    for i in range(len(x)):
        for j in range(len(x[i])):
            r[i][j] = operations[op](x[i][j], y[i][j])
    return r


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(entities.ID)
    def visit(self, node):

        return self.memory_stack.get(node.id)

    @when(entities.IDAt)
    def visit(self, node):
        matrix = self.memory_stack.get(node.id)
        index1 = self.visit(node.index1)
        index2 = self.visit(node.index2)
        return matrix[index1][index2]

    @when(entities.Condition)
    def visit(self, node):
        if self.visit(node.bool_expression):
            return self.visit(node.statement1)
        else:
            if node.statement2 is not None:
                return self.visit(node.statement2)
            return None

    @when(entities.Matrix)
    def visit(self, node):
        if node.type is None:
            m = self.visit(node.content)
        elif node.type == "zeros":
            m = [[0 for i in range(node.dim)] for j in range(node.dim)]
        elif node.type == "ones":
            m = [[1 for i in range(node.dim)] for j in range(node.dim)]
        elif node.type == "eye":
            m = [[0 for i in range(node.dim)] for j in range(node.dim)]
            for i in range(node.dim):
                m[i][i] = 1

        # import code; code.interact(local=dict(globals(), **locals()))
        return m

    @when(entities.Number)
    def visit(self, node):
        return node.value

    @when(entities.BinaryOperation)
    def visit(self, node):
        r1 = self.visit(node.left)
        r2 = self.visit(node.right)
        op = node.operator
        # import code; code.interact(local=dict(globals(), **locals()))
        return operations[op](r1, r2)

    @when(entities.UnaryOperation)
    def visit(self, node):
        # import code; code.interact(local=dict(globals(), **locals()))
        op = node.operator
        arg = self.visit(node.arg)
        return operations[op + "u"](arg)

    @when(entities.Assignment)
    def visit(self, node):
        # expr = node.expr.accept(self)
        expr = self.visit(node.right)
        op = node.operator
        var = self.memory_stack.get(node.left.id)
        # if var is None:
        value = operations[op](var, expr)
        self.memory_stack.set(node.left.id, value)
        # import code; code.interact(local=dict(globals(), **locals()))
        return value

    @when(entities.Relation)
    def visit(self, node):
        op = node.operator
        left = self.visit(node.left)
        right = self.visit(node.right)
        return operations[op](left, right)

    @when(entities.WhileLoop)
    def visit(self, node):
        try:
            condition = self.visit(node.expr)
            self.memory_stack.push(Memory("WhileLoop"))
            while condition:
                try:
                    self.visit(node.prog)
                    condition = self.visit(node.expr)
                except BreakException:
                    break
                except ContinueException:
                    continue
        finally:
            self.memory_stack.pop()

    @when(entities.ForLoop)
    def visit(self, node):
        try:
            beg = self.visit(node.beg)
            end = self.visit(node.end)
            self.memory_stack.push(Memory("ForLoop"))
            for i in range(beg, end):
                try:
                    self.memory_stack.set(node.id, i)
                    self.visit(node.prog)
                except BreakException:
                    break
                except ContinueException:
                    continue
        finally:
            self.memory_stack.pop()

    @when(entities.Return)
    def visit(self, node):
        value = self.visit(node.variable)
        raise ReturnValueException(value)

    @when(entities.Break)
    def visit(self, node):
        raise BreakException()

    @when(entities.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(entities.Print)
    def visit(self, node):
        list = self.visit(node.list)
        print(list if len(list) > 1 else list[0])

    @when(entities.Empty)
    def visit(self, node):
        pass

    @when(entities.Program)
    def visit(self, node):
        self.visit(node.statement)
        self.visit(node.program)
        return node

    @when(entities.List)
    def visit(self, node):
        return [self.visit(x) for x in node.get_value()]
        # return node.get_value() =

    @when(entities.List2D)
    def visit(self, node):
        # return self.visit(node.get_value()[0])
        return [self.visit(x) for x in node.get_value()]
        # return node.get_value()
