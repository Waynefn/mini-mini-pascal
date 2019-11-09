OP = {'ADD': '+', 'SUB': '-', 'MLT': '*', 'DIV': '/', 'EQL': '==', 'GRT': '>', 'LES': '<'}


class Machine:
    def __init__(self, asm_tokens):
        self.pc = 0
        self.stack = [] * 2
        self.memory = [None] * 26
        self.asm_tokens = asm_tokens

    def run(self):
        while True:
            cmd = self.asm_tokens[self.pc]
            if cmd.unit_type == 'GET':
                self.memory[cmd.value] = int(input('@{}?'.format(cmd.value)))
            elif cmd.unit_type == 'PUT':
                print("@{}={}".format(cmd.value, self.memory[cmd.value]))
            elif cmd.unit_type == 'LOD':
                self.stack.append(self.memory[cmd.value])
            elif cmd.unit_type == 'LDC':
                self.stack.append(cmd.value)
            elif cmd.unit_type == 'STR':
                self.memory[cmd.value] = self.stack.pop()
            elif cmd.unit_type == 'UJP':
                self.pc = cmd.value - 1
            elif cmd.unit_type == 'CJP':
                if self.stack[-1] == 0:
                    self.pc = cmd.value - 1
            elif cmd.unit_type in ['ADD', 'SUB', 'MLT', 'DIV', 'EQL', 'GRT', 'LES']:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(eval("int({}{}{})".format(a, OP[cmd.unit_type], b)))
            else:
                raise SyntaxError('M Error@{}'.format(cmd))
            self.pc += 1
            if self.pc >= len(self.asm_tokens):
                print("Machine exits.")
                return 0
