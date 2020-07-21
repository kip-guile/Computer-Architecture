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

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print(f'usage: {sys.argv[0]} filename')
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                     num = line.split('#', 1)[0]
                     if num.strip() == '':
                         continue

                    self.ram[address] = int(num, 2)
                    address += 1
        
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.srgb[1]} not found')
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
            return self.reg[reg_a]
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
            self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if cmd == HLT:
                running = False

            elif cmd == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif cmd == PRN:
                print(self.reg[operand_a])
                self.pc += 2

            elif cmd == MUL:
                MULVAL = self.alu(self, self.reg[operand_a], self.reg[operand_b])
                print('multiplied value ==>' MULVAL)
                self.pc += 3
                self.alu('MUL' operand_a,operand_b)
                self.pc +=3

            else:
                print('unknown instruction')
                sys.exit(1)
