import entities

class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)


class TypeChecker(NodeVisitor):

    def visit_ID(self, node):
        pass

    def visit_Number(selfself, node):
        pass

    def visit_IDAt(self, node):
        self.visit(node.index1)
        self.visit(node.index2)
        if not node.index1.isNumber or not node.index2.isNumber:
            print(f"Error in line {node.line}: Indexes are not numbers!")

        if (isinstance(node.index1, entities.Number) and node.index1.type == 'float') \
                or (isinstance(node.index2, entities.Number) and node.index2.type == 'float'):
            print(f"Error in line {node.line}: Float indexes not permitted!")

    def visit_Condition(self, node):
        self.visit(node.bool_expression)
        if node.bool_expression.notBoolean:
            print(f"Error in line {node.line}: Condition is not of boolean type!")
        self.visit(node.statement1)
        self.visit(node.statement2)

    #TODO
    def visit_Matrix(self, node):
        pass

    #TODO
    def visit_BinaryOperation(self, node):
        pass

    def visit_UnaryOperation(self, node):
        self.visit(node.arg)
        if node.operation == '\'' and not node.arg.isMatrix:
            print(f"Error in line {node.line}: Wrong transpose argument (of matrix type required)!")
        if node.operation == '.-' and not node.arg.isMatrix:
            print(f"Error in line {node.line}: Wrong .- argument (of matrix type required)!")

        if node.operation == '.-' and not node.arg.isNumber:
            print(f"Error in line {node.line}: Wrong - argument (of number type required)!")


    def visit_Assignment(self, node):

        self.visit(node.left)
        self.visit(node.right)

        if not isinstance(node.left, entities.IDAt) or not isinstance(node.left, entities.ID):
            print(f"Error in line {node.line}: Left arg of assignment have to be variable!")

        if node.operator != '=' and not node.right.isNumber:
            print(f"Error in line {node.line}: Such assignment requires right arg of number type!")


    def visit_Relation(self, node):

        self.visit(node.left)
        self.visit(node.right)

        if not node.left.isNumeric or not node.left.isNumeric:
            print(f"Error in line {node.line}: numeric expressions required in relations!")

    def visit_WhileLoop(self, node):

        self.visit(node.expr)
        self.visit(node.prog)

        if not node.expr.isBoolean:
            print(f"Error in line {node.line}: while condition has to be of boolean type!")

    def visit_ForLoop(self, node):

        self.visit(node.id)
        self.visit(node.beg)
        self.visit(node.end)
        self.visit(node.prog)

        if not isinstance(node.id, entities.ID):
            print(f"Error in line {node.line}: Iterator has to be a variable!")

        if node.beg.isNumber:
            print(f"Error in line {node.line}: Beginning value of iterator has to be a number!")

        if node.end.isNumber:
            print(f"Error in line {node.line}: End value of iterator has to be a number!")



    def visit_Print(self, node):

        self.visit(node.list)


    def visit_Program(self, node):

        self.visit(node.statement)
        self.visit(node.program)

    def visit_List(self, node):
        pass

    def visit_List2D(self, node):
        list_of_vectors = node.get_value()
        list_of_length = []
        for vector in list_of_vectors:
            self.visit(vector)
            list_of_length.append(len(vector.get_value()))

        ok = True
        for i in range(list_of_length) -1:
            if list_of_length[i] != list_of_length[i+1]:
                ok = False

        if not ok:
            print(f"Error in line {node.line}: Vectors of different lengths!")

    def visit_Empty(self, node):
        pass