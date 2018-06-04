import entities
import symbol_table
import types_


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass


class TypeChecker(NodeVisitor):
    table = symbol_table.SymbolTable(None, 'program')

    def __init__(self):
        self.errors = False

    def visit_ID(self, node):
        symbol = self.table.get(node.id)
        if not symbol:
            return types_.Id()
        return symbol.symbol_type

    def visit_Number(self, node):
        if node.type == 'integer':
            return types_.Int()
        return types_.Float()

    def visit_Matrix(self, node):

        if node.type == None:
            return self.visit(node.content)

        elif node.type == 'zeros':
            node.matrix = [0 for i in range(node.dim)] * node.dim

        elif node.type == 'ones':
            node.matrix = [1 for i in range(node.dim)] * node.dim

        elif node.type == 'eye':
            node.matrix = [[1 if i == j else 0 for i in range(node.dim)] for j in range(node.dim)]

            return types_.Matrix(node.dim, node.dim, types_.Int())


    def visit_IDAt(self, node):
        type_index1 = self.visit(node.index1)
        type_index2 = self.visit(node.index2)
        index1 = None
        index2 = None
        if not type_index1.is_integer:
            print(f"Error in line {node.line}: first index is not an integer!")
        else:
            index1 = node.index1.value

        if not type_index2.is_integer:
            print(f"Error in line {node.line}: second index is not an integer!")
        else:
            index2 = node.index2.value

        id = self.visit_ID(node)
        if id.is_id():
            print(f"Error in line {node.line}: variable {node.id} not known!")
        elif not id.is_matrix():
            print(f"Error in line {node.line}: variable {node.id} not a matrix!")
        else:
            if index1 < id.x and index2 < id.y:
                return id.element_type()
            else:
                print(f"Error in line {node.line}: index out of bounds!")

        return types_.Int()

    def visit_Condition(self, node):

        bool = self.visit(node.bool_expression)

        if not bool.is_boolean():
            print(f"Error in line {node.line}: Condition is not of boolean type!")

        self.table.pushScope('condition')
        self.visit(node.statement1)
        self.table.popScope()
        self.table.pushScope('condition')
        self.visit(node.statement2)
        self.table.popScope()

    def visit_BinaryOperation(self, node):
        right = self.visit(node.right)
        left = self.visit(node.left)
        if node.operator in ['.+', '.-', '.*', './']:

            if left.is_matrix() and  right.is_matrix() \
                    and (left.x != right.x or left.y != right.y):
                print(f"Error in line {node.line}: Matrix binary operation require equal dimensions!")

            return right

        else:
            if not right.is_numeric():
                print(f"Error in line {node.line}: {node.operator} require number arguments!")
                return types_.Int()
            if not left.is_numeric():
                print(f"Error in line {node.line}: {node.operator} require number arguments!")
                return types_.Int()
            return right

    def visit_UnaryOperation(self, node):

        arg = self.visit(node.arg)
        if node.operator == '\'':
            if not arg.is_matrix():
                print(f"Error in line {node.line}: Wrong transpose argument (of matrix type required)!")
            else:
                return types_.Matrix(-1,-1,None)

        if node.operator == '.-':
            if not arg.is_matrix():
                print(f"Error in line {node.line}: Wrong .- argument (of matrix type required)!")
            else:
                return types_.Matrix(-1, -1, None)

        if node.operator == '-':
            if not arg.is_numeric():
                print(f"Error in line {node.line}: Wrong - argument (of number type required)!")
                return types_.Int()
            else:
                return arg

    def visit_Assignment(self, node):

        if not isinstance(node.left, entities.ID):
            print(f"Error in line {node.line}: Left operand is not a variable!")
            return

        right = self.visit(node.right)
        if node.operator == '=':
            self.table.put(node.left.id, symbol_table.VariableSymbol(right, node.right))
            return

        if node.operator != '=':
            id = self.table.get(node.left.id)
            if not id:
                print(f"Error in line {node.line}: Unknown variable!")
            if not id.symbol_type.is_numeric():
                print(f"Error in line {node.line}: Such assignment requires right arg of number type!")
        return

    def visit_Relation(self, node):

        left = self.visit(node.left)
        if not left.is_numeric():
            print(f"Error in line {node.line}: left operand of relation is not numeric!")

        right = self.visit(node.right)
        if not right.is_numeric():
            print(f"Error in line {node.line}: right operand of relation is not numeric!")

        return types_.Boolean()

    def visit_WhileLoop(self, node):

        expr = self.visit(node.expr)

        if not expr.is_boolean():
            print(f"Error in line {node.line}: while condition has to be of boolean type!")

        self.table.pushScope('loop')
        prog = self.visit(node.prog)
        self.table.popScope()

    def visit_ForLoop(self, node):

        self.table.pushScope('loop')
        beg = self.visit(node.beg)
        end = self.visit(node.end)

        if not beg.is_integer():
            print(f"Error in line {node.line}: Beginning value of iterator has to be an integer!")

        if not end.is_integer():
            print(f"Error in line {node.line}: End value of iterator has to be a number!")

        self.visit(node.prog)
        self.table.popScope()

    def visit_Print(self, node):

        self.visit(node.list)

    def visit_Program(self, node):

        self.visit(node.statement)
        self.visit(node.program)

    def visit_List(self, node):
        length = len(node.get_value())
        types = []
        for n in node.get_value():
            types.append(self.visit(n))
        diff = False
        for i in range(length - 1):
            if type(types[i]) != type(types[i + 1]):
                diff = True

        if diff:
            return types_.List(length, None)
        return types_.List(length, types[0])

    def visit_List2D(self, node):
        list_of_vectors = node.get_value()
        list_of_length = []
        list_of_type = []
        for vector in list_of_vectors:
            l_type = self.visit(vector)
            list_of_length.append(l_type.length)
            list_of_type.append(l_type.element_type)
        ok = True
        diff = False
        for i in range(len(list_of_length) - 1):
            if list_of_length[i] != list_of_length[i + 1]:
                ok = False
            if type(list_of_type[i]) != type(list_of_type[i + 1]):
                diff = True
        if None in list_of_type:
            diff = True

        if not ok:
            print(f"Error in line {node.line}: Vectors of different lengths!")

        if diff:
            print(f"Error in line {node.line}: All variables in a matrix has to be of one type!")
            return types_.Matrix(len(list_of_length), list_of_length[0], types_.Int())

        return types_.Matrix(len(list_of_length), list_of_length[0], list_of_type[0])

    def visit_Empty(self, node):
        return 'empty'

    def visit_Break(self, node):
        if not self.table.is_inside_loop():
            print(f"Error in line {node.line}: Break outside a loop")
        return 'break'

    def visit_Contnue(self, node):
        if not self.table.is_inside_loop():
            print(f"Error in line {node.line}: Continue outside a loop")
        return 'continue'

    def visit_Return(self, node):

        if node.variable:
            n_type = self.visit(node.variable)
            if n_type not in ['integer', 'float', 'boolean'] and not 'matrix' in n_type:
                print(f"Error in line {node.line}: Wrong returned type!")
        return 'return'
