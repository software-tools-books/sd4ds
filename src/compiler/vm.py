"""Virtual machine specification."""

import sys

from architecture import NUM_REG, OP_CODES, OP_MASK, OP_SHIFT, RAM_LEN

COLUMNS = 4


class VirtualMachine:
    def __init__(self):
        self.ip = 0
        self.reg = [0] * NUM_REG
        self.ram = [0] * RAM_LEN
        self.prompt = ">>"

    def initialize(self, program):
        assert len(program) <= len(self.ram), "Program is too long for memory"
        self.ip = 0
        self.reg = [0] * NUM_REG
        for i in range(len(self.ram)):
            self.ram[i] = program[i] if i < len(program) else 0

    def fetch(self):
        assert (0 <= self.ip) and (self.ip < RAM_LEN)
        instruction = self.ram[self.ip]
        self.ip += 1
        op = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return op, arg0, arg1

    def run(self):
        running = True
        while running:
            op, arg0, arg1 = self.fetch()
            assert op in OP_CODES
            op = OP_CODES[op]

            if op.instr == "hlt":
                running = False

            elif op.instr == "ldc":
                self.assertIsRegister(arg0)
                self.reg[arg0] = arg1

            elif op.instr == "ldr":
                self.assertIsRegister(arg0)
                self.assertIsRegister(arg1)
                self.reg[arg0] = self.ram[self.reg[arg1]]

            elif op.instr == "cpy":
                self.assertIsRegister(arg0)
                self.assertIsRegister(arg1)
                self.reg[arg0] = self.reg[arg1]

            elif op.instr == "str":
                self.assertIsRegister(arg0)
                self.assertIsRegister(arg1)
                self.assertIsAddress(self.reg[arg1])
                self.ram[self.reg[arg1]] = self.reg[arg0]

            elif op.instr == "add":
                self.assertIsRegister(arg0)
                self.assertIsRegister(arg1)
                self.reg[arg0] += self.reg[arg1]

            elif op.instr == "sub":
                self.assertIsRegister(arg0)
                self.assertIsRegister(arg1)
                self.reg[arg0] -= self.reg[arg1]

            elif op.instr == "beq":
                self.assertIsRegister(arg0)
                self.assertIsAddress(arg1)
                if self.reg[arg0] == 0:
                    self.ip = arg1

            elif op.instr == "bne":
                self.assertIsRegister(arg0)
                self.assertIsAddress(arg1)
                if self.reg[arg0] != 0:
                    self.ip = arg1

            elif op.instr == "prr":
                self.assertIsRegister(arg0)
                print(self.prompt, self.reg[arg0])

            elif op.instr == "prm":
                self.assertIsRegister(arg0)
                self.assertIsAddress(self.reg[arg0])
                print(self.prompt, self.ram[self.reg[arg0]])

            else:
                assert False, f"Unknown op {op}"

    def show(self, writer=sys.stdout):
        # Registers
        for (i, r) in enumerate(self.reg):
            print(f"R{i:02} = {r:06x}", file=writer)

        # How much RAM to show
        top = len(self.ram) - 1
        while (top >= 0) and (self.ram[top] == 0):
            top -= 1

        # Show RAM
        base = 0
        while base <= top:
            output = f"{base:04x}:"
            for i in range(COLUMNS):
                output += f"    {self.ram[base+i]:06x}"
            print(output, file=writer)
            base += COLUMNS

    def assertIsRegister(self, reg):
        assert (0 <= reg) and (reg < len(self.reg)), f"Invalid register {reg}"

    def assertIsAddress(self, addr):
        assert (0 <= addr) and (addr < len(self.ram)), f"Invalid register {addr}"


if __name__ == "__main__":
    instructions = [int(ln.strip(), 16) for ln in sys.stdin.readlines()]
    vm = VirtualMachine()
    vm.initialize(instructions)
    vm.show()
    print("-" * 16)
    vm.run()
    print("-" * 16)
    vm.show()
