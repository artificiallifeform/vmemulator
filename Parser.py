class Parser:
    def __init__(self, command):
        self.command = command
        self.type = ''
        self.define_type()

    def define_type(self):
        if self.command.startswith('push') or self.command.startswith('pop'):
            self.type = 'MEMORY_C'
        else:
            self.type = 'ARITHM_C'
        
    
    def get_command(self):
        return {"command": self.command.split(' '), "type": self.type}

