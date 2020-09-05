class Code:
    condition_iter = 1

    def __init__(self, command, filename, ops_on_stack):
        self.command = command["command"]
        self.type = command["type"]
        self.filename = filename
        self.operations = ops_on_stack

    def execute_operation(self):
        if self.type == 'MEMORY_C':
            self.operate_on_stack()
        elif self.type == 'ARITHM_C':
            self.generate_arithmetic_c(self.command[0])

    def operate_on_stack(self):
        if self.command[1] == 'static':
            operation = self.command[0] + '_' + self.command[1]
            commands = self.operations[operation](self.filename, self.command[2])
            commands.insert(0, "// " + " ".join(self.command))
            self._write_to_file('\n'.join(commands))
            return

        operation = self.command[0] + '_' + self.command[1]
        commands = self.operations[operation](self.command[2])
        commands.insert(0, "// " + " ".join(self.command))
        self._write_to_file('\n'.join(commands))
        
        
    def generate_arithmetic_c(self, opType):
        commands = []

        if opType == 'add':
            commands = self.operations[opType]()
        elif opType == 'sub':
            commands = self.operations[opType]()
        elif opType == 'neg':
            commands = self.operations[opType]()
        elif opType == 'eq':
            commands = self.operations[opType](Code.condition_iter)
            Code.condition_iter += 1
        elif opType == 'lt':
            commands = self.operations[opType](Code.condition_iter)
            Code.condition_iter += 1
        elif opType == 'gt':
            commands = self.operations[opType](Code.condition_iter)
            Code.condition_iter += 1
        elif opType == 'and':
            commands = self.operations[opType]()
        elif opType == 'or':
            commands = self.operations[opType]()
        elif opType == 'not':
            commands = self.operations[opType]()

        commands.insert(0,'// Arithmetic command')
        self._write_to_file('\n'.join(commands))

    def _write_to_file(self, commands):
        with open(self.filename+".asm", 'a') as f:
            f.write(commands + '\n')

        