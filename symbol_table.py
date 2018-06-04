from copy import deepcopy

class VariableSymbol():

    def __init__(self, symbol_type, symbol_content):
        self.symbol_type = symbol_type
        self.symbol_content = symbol_content

    def get(self):
        return self.symbol_content


class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.scope = {}
        self.name = name

    def put(self, name, symbol):
        self.scope[name] = symbol

    def get(self, name):
        current = self
        while(current != None):
            if current.scope.get(name, None):
                return current.scope[name]
            current = current.parent
        return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        new = deepcopy(self)
        self.parent = new
        self.name = name
        self.scope = {}


    def popScope(self):
        self.name = self.parent.name
        self.scope = self.parent.scope
        self.parent = self.parent.parent

    def is_inside_loop(self):

        current_scope = self
        while current_scope:
            if current_scope.name == 'loop':
                return True
            current_scope = current_scope.parent
        return False