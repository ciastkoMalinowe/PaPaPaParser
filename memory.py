class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.memory = {}

    def has_key(self, name):  # variable name
        return name in self.memory #self.memory.has_key(name)

    def get(self, name):         # gets from memory current value of variable <name>
        return self.memory.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value

class MemoryStack:

    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        if memory:
            self.stack.append(memory)
        else:
            self.stack.append(Memory("Global"))


    def get(self, name):             # gets from memory stack current value of variable <name>
        length = len(self.stack)
        for i in range(length):
            id = length - i - 1
            if self.stack[id].has_key(name):
                return self.stack[id].get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        length = len(self.stack)
        for i in range(length):
            id = length - i - 1
            if self.stack[id].has_key(name):
                self.stack[id].put(name, value)
            else:
                self.insert(name, value)
        return None

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        return self.stack.pop()
