import entities
import symbol_table

class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass


class TypeChecker(NodeVisitor):

    table = symbol_table.SymbolTable(None, 'program')

    def visit_ID(self, node):
        symbol = self.table.get(node.id)

        if not symbol:
            return 'id'
        return symbol.symbol_type

    def visit_Number(self, node):
        return node.type

    def visit_Matrix(self, node):

        if node.type == None:
            l_type = self.visit(node.content)

            if 'list2D' in l_type:
                details = l_type.split(' ')
                if details[2] == 'different':
                    print(f"Error in line {node.line}: All variables in a matrix has to be of one type!")
                    return f'matrix {details[1]} {details[2]} integer'
                return f'matrix {details[1]} {details[2]} {details[3]}'
            else:
                print(f"Error in line {node.line}: Wrong matrix initialisation (list2D of fun required)!")

        elif node.type == 'zeros':
            node.matrix = [0 for i in range(node.dim)] * node.dim

        elif node.type == 'ones':
            node.matrix = [1 for i in range(node.dim)] * node.dim

        elif node.type == 'eye':
            node.matrix = [[ 1 if i==j else 0 for i in range(node.dim)] for j in range(node.dim)]

        return f'matrix {node.dim} {node.dim} integer'

    def visit_IDAt(self, node):
        type_index1 = self.visit(node.index1)
        type_index2 = self.visit(node.index2)
        index1 = None
        index2 = None
        if type_index1 != 'integer':
            print(f"Error in line {node.line}: first index is not an integer!")
        else:
            index1 = node.index1.value

        if type_index2 != 'integer':
            print(f"Error in line {node.line}: second index is not an integer!")
        else:
            index2 = node.index2.value

        id = self.visit_ID(node)
        if id == 'id':
            print(f"Error in line {node.line}: variable {node.id} not known!")
        elif 'matrix' not in id:
            print(f"Error in line {node.line}: variable {node.id} not a matrix!")
        else:
            details = id.split(' ')
            if index1 < int(details[1]) and index2 < int(details[2]):
                return details[3]
            else:
                print(f"Error in line {node.line}: index out of bounds!")

        return 'integer'


    def visit_Condition(self, node):

        bool = self.visit(node.bool_expression)

        if bool != 'boolean':
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

            right_x = None
            right_y = None
            left_x = None
            left_y = None

            if 'matrix' in right:
                right_details = right.split(' ')
                right_x = right_details[1]
                right_y = right_details[2]

            if 'matrix' in left:
                left_details = left.split(' ')
                left_x = left_details[1]
                left_y = left_details[2]

            if None not in [right_x, right_y, left_x, left_y] \
                    and (left_x != right_x or left_y != right_y):
                print(f"Error in line {node.line}: Matrix binary operation require equal dimensions!")

            return right

        else:
            if right not in ['integer', 'float']:

                print(f"Error in line {node.line}: {node.operator} require number arguments!")
                return 'integer'
            if left not in ['integer', 'float']:

                print(f"Error in line {node.line}: {node.operator} require number arguments!")
                return 'integer'
            return right


    def visit_UnaryOperation(self, node):

        arg = self.visit(node.arg)
        if node.operation == '\'':
            if 'matrix' not in arg:
                print(f"Error in line {node.line}: Wrong transpose argument (of matrix type required)!")
            else:
                return 'matrix -1 -1 None'

        if node.operation == '.-':
            if 'matrix' not in arg:
                print(f"Error in line {node.line}: Wrong .- argument (of matrix type required)!")
            else:
                return 'matrix -1 -1 None'

        if node.operation == '-':
            if arg not in ['integer', 'float']:
                print(f"Error in line {node.line}: Wrong - argument (of number type required)!")
                return 'integer'
            else:
                return arg


    def visit_Assignment(self, node):

        left = self.visit(node.left)
        if not isinstance(node.left, entities.ID):
            print(f"Error in line {node.line}: Left operand is not a variable!")
            return 'assignment'

        right = self.visit(node.right)
        if node.operator == '=':
            self.table.put(node.left.id, symbol_table.VariableSymbol(right, node.right))
            return 'assignment'

        if node.operator != '=':
            id = self.table.get(node.left.id)
            if not id:
                print(f"Error in line {node.line}: Unknown variable!")
            if id.symbol_type not in ['integer', 'float']:
                print(f"Error in line {node.line}: Such assignment requires right arg of number type!")
        return 'assignment'


    def visit_Relation(self, node):

        left = self.visit(node.left)
        if left not in ['integer', 'float']:
            print(f"Error in line {node.line}: left operand of relation is not numeric!")

        right = self.visit(node.right)
        if right not in ['integer', 'float']:
            print(f"Error in line {node.line}: right operand of relation is not numeric!")

        return 'boolean'


    def visit_WhileLoop(self, node):

        expr = self.visit(node.expr)

        if expr != 'boolean':
            print(f"Error in line {node.line}: while condition has to be of boolean type!")

        self.table.pushScope('loop')
        prog = self.visit(node.prog)
        self.table.popScope()
        return 'loop'



    def visit_ForLoop(self, node):

        self.table.pushScope('loop')
        id = self.visit(node.id)
        beg = self.visit(node.beg)
        end = self.visit(node.end)
        self.visit(node.prog)
        self.table.popScope()

        if id != 'id':
            print(f"Error in line {node.line}: Iterator has to be a variable!")

        if beg != 'integer':
            print(f"Error in line {node.line}: Beginning value of iterator has to be an integer!")

        if end != 'integer':
            print(f"Error in line {node.line}: End value of iterator has to be a number!")
        return 'loop'


    def visit_Print(self, node):

        self.visit(node.list)
        return 'print'


    def visit_Program(self, node):

        self.table.pushScope('program')
        self.visit(node.statement)
        self.table.popScope()
        self.visit(node.program)
        return 'program'

    def visit_List(self, node):
        length = len(node.get_value())
        types = []
        for n in node.get_value():
            types.append(self.visit(n))
        diff = False
        for i in range(length - 1):
            if types[i] != types[i+1]:
                diff = True

        if diff:
            return f'list {length} different'
        return f'list {length} {types[0]}'

    def visit_List2D(self, node):
        list_of_vectors = node.get_value()
        list_of_length = []
        list_of_type = []
        for vector in list_of_vectors:
            l_type = self.visit(vector)
            details = l_type.split(' ')
            list_of_length.append(details[1])
            list_of_type.append(details[2])

        ok = True
        diff = False
        for i in range(len(list_of_length) -1):
            if list_of_length[i] != list_of_length[i+1]:
                ok = False
            if list_of_type[i] != list_of_type[i+1]:
                diff = True
        if 'different' in list_of_type:
            diff = True

        if not ok:
            print(f"Error in line {node.line}: Vectors of different lengths!")

        if diff:
            return f'list2D {len(list_of_length)} {list_of_length[0]} different'

        return f'list2D {len(list_of_length)} {list_of_length[0]} {list_of_type[0]}'

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
            if n_type not in ['integer','float', 'boolean'] and not 'matrix' in n_type:
                print(f"Error in line {node.line}: Wrong returned type!")
        return 'return'