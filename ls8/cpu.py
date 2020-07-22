"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        self.branchtable = {}
        self.branch_operations()

    def LDI(self, a, b, c):
        self.reg[a] = b
        self.pc += 3

    def MUL(self, a, b):
        self.alu('MUL', a, b)
        self.pc += 3

    def PRN(self, a, b):
        print(self.reg[a])
        self.pc += 2

    def branch_operations(self):
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b00000001] = self.HLT

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self, arg):
        """Load a program into memory."""

        program = []

        try:
            address = 0
            with open(arg[1]) as f:
                for line in f:
                    # split before comment
                    # convert to a number splitting and stripping
                    num = line.split('#')[0].strip()
                    if num == '':
                        continue  # ignore blank lines

                    # print num
                    value = int(num, 2)  # ,2
                    program.append(value)

        except FileNotFoundError:
            print(f'{arg[0]}: {arg[1]} not found')
            sys.exit(2)

        # store val in memory at the given address
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            cmd = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if cmd == HLT:
                running = False

            # elif cmd == LDI:
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3

            # elif cmd == PRN:
            #     print(self.reg[operand_a])
            #     self.pc += 2

            # elif cmd == MUL:
            #     # MULVAL = self.alu(
            #     #     self, self.reg[operand_a], self.reg[operand_b])
            #     # print('multiplied value ==>', MULVAL)
            #     # self.pc += 3
            #     self.alu('MUL', operand_a, operand_b)
            #     self.pc += 3

            else:
                elif IR not in self.branchtable:
                    print('unknown instruction')
                    sys.exit(1)

                else:
                    self.branchtable[cmd](operand_a, operand_b)
