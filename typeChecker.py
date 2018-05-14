import entities

class NodeVisitor(object):
    def visit(self, node, stack):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, stack)

    def generic_visit(self, node, stack):
        pass


class TypeChecker(NodeVisitor):

# *****************************
# ...........helpers...........
# *****************************


    def _not_number(self, t):
        if not isinstance(t, entities.Number) \
                and not isinstance(t, entities.ID) \
                and not isinstance(t, entities.IDAt):
            return True
        return False

    def _not_boolean(self, t):
        if not isinstance(t, entities.Assignment) \
                and not isinstance(t, entities.ID):
            return True
        return False

    def _not_matrix(self, t):
        if not isinstance(t, entities.Matrix) \
                and not isinstance(t, entities.ID):
            return True
        return False

    def _not_id(self, t):
        if not isinstance(t, entities.IDAt) \
                and not isinstance(t, entities.ID):
            return True
        return False

    def _not_in_loop(self, stack):

        if len(stack) == 0 \
                or not isinstance(stack[-1], entities.ForLoop) \
                or not isinstance(stack[-1], entities.ForLoop):
            return True
        return False

    def _is_float(self,t):
        if isinstance(t, entities.Number) and t.type == 'float':
            return True
        return False


#*****************************
# ......visit functions.......
#*****************************

    def visit_Matrix(self, node, stack):

        if node.type == None:
            self.visit(node.content, stack)
            lengths = []
            for l in node.content.get_value():
                lengths.append(len(l.get_value()))
                for i in l.get_value():
                    if self._not_number(i):
                        print(f"Error in line {i.line}: Not number!")

    def visit_IDAt(self, node, stack):
        self.visit(node.index1, stack)
        self.visit(node.index2, stack)
        if self._not_number(node.index1) or self._not_number(node.index2):
            print(f"Error in line {node.line}: Indexes are not numbers!")

        if self._is_float(node.index1) or self._is_float(node.index2):
            print(f"Error in line {node.line}: Float indexes not permitted!")

    def visit_Condition(self, node, stack):

        self.visit(node.bool_expression, stack)

        if self._not_boolean(node.bool_expression):
            print(f"Error in line {node.line}: Condition is not of boolean type!")
        self.visit(node.statement1, stack)
        self.visit(node.statement2, stack)

    def visit_BinaryOperation(self, node, stack):
        self.visit(node.right, stack)
        self.visit(node.left, stack)
        if node.operator in ['.+', '.-', '.*', './']:
            if self._not_matrix(node.left) or self._not_matrix(node.right):
                print(f"Error in line {node.line}: {node.opeator} require matrix arguments!")
            if isinstance(node.left, entities.Matrix) and isinstance(node.right, entities.Matrix):
                if node.left.x != node.right.x or node.left.y != node.left.y:
                    print(f"Error in line {node.line}: Matrix binary operation require equal dimensions!")
        else:
            if self._not_number(node.left) or self._not_number(node.right):
                print(f"Error in line {node.line}: {node.operator} require number arguments!")


    def visit_UnaryOperation(self, node, stack):
        self.visit(node.arg, stack)
        if node.operation == '\'' and self._not_matrix(node.arg):
            print(f"Error in line {node.line}: Wrong transpose argument (of matrix type required)!")
        if node.operation == '.-' and self._not_matrix(node.arg):
            print(f"Error in line {node.line}: Wrong .- argument (of matrix type required)!")

        if node.operation == '.-' and self._not_number(node.arg):
            print(f"Error in line {node.line}: Wrong - argument (of number type required)!")


    def visit_Assignment(self, node, stack):

        self.visit(node.left, stack)
        self.visit(node.right, stack)

        if self._not_id(node.left):
            print(f"Error in line {node.line}: Left arg of assignment have to be variable!")

        if node.operator != '=' and self._not_number(node.right):
            print(f"Error in line {node.line}: Such assignment requires right arg of number type!")


    def visit_Relation(self, node, stack):

        self.visit(node.left, stack)
        self.visit(node.right, stack)

        if self._not_number(node.left) or self._not_number(node.right):
            print(f"Error in line {node.line}: numeric expressions required in relations!")

    def visit_WhileLoop(self, node, stack):

        self.visit(node.expr, stack)
        stack.append(node)
        self.visit(node.prog, stack)
        stack = stack[:-1]

        if self._not_boolean(node.expr):
            print(f"Error in line {node.line}: while condition has to be of boolean type!")

    def visit_ForLoop(self, node, stack):

        self.visit(node.id, stack)
        self.visit(node.beg, stack)
        self.visit(node.end, stack)
        stack.append(node)
        self.visit(node.prog, stack)
        stack = stack[:-1]

        if self._not_id(node.id):
            print(f"Error in line {node.line}: Iterator has to be a variable!")

        if self._not_number(node.beg):
            print(f"Error in line {node.line}: Beginning value of iterator has to be a number!")


        if self._not_number(node.end):
            print(f"Error in line {node.line}: End value of iterator has to be a number!")



    def visit_Print(self, node, stack):

        self.visit(node.list, stack)


    def visit_Program(self, node, stack):

        stack.append(node.statement)
        self.visit(node.statement, stack)
        stack = stack[:-1]
        self.visit(node.program, stack)

    def visit_List(self, node, stack):
        pass

    def visit_List2D(self, node, stack):
        list_of_vectors = node.get_value()
        list_of_length = []
        for vector in list_of_vectors:
            self.visit(vector, stack)
            list_of_length.append(len(vector.get_value()))

        ok = True
        for i in range(len(list_of_length) -1):
            if list_of_length[i] != list_of_length[i+1]:
                ok = False

        if not ok:
            print(f"Error in line {node.line}: Vectors of different lengths!")

    def visit_Empty(self, node, stack):
        pass


    def visit_Break(self, node, stack):
        if self._not_in_loop(stack):
            print(f"Error in line {node.line}: Break outside a loop")


    def visit_Contnue(self, node, stack):
        if self._not_in_loop(stack):
            print(f"Error in line {node.line}: Continue outside a loop")

    def visit_Return(self, node, stack):

        if node.variable:
            self.visit(node.variable, stack)

            if self._not_matrix(node.variable) \
                or self._not_number(node.variable) \
                or self._not_boolean(node.variable):
                print(f"Error in line {node.line}: Wrong returned type!")