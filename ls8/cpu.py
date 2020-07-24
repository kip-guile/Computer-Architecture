"""CPU functionality."""

import sys

HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        self.branchtable = {}
        self.branch_operations()
        # initialize stack pointer
        self.stack_pointer = 0xF3
        self.FLG = 0b00000000

    # Branch ops
    def LDI(self, a, b):
        self.reg[a] = b
        self.pc += 3

    def MUL(self, a, b):
        self.alu('MUL', a, b)
        self.pc += 3

    def CMP(self, a, b):
        self.alu('CMP', a, b)
        self.pc += 3

    def PRN(self, a, b):
        print(self.reg[a])
        self.pc += 2

    def CALL(self, a, b):
        self.stack_pointer -= 1
        return_address = self.pc + 2
        self.ram_write(self.stack_pointer, return_address)
        self.pc = self.reg[a]

    def RET(self, a, b):
        stack_value = self.ram[self.stack_pointer]
        self.pc = stack_value

    # Stack ops
    def POP(self, a, b):
        stack_value = self.ram[self.stack_pointer]
        self.reg[a] = stack_value
        # increase pointer once we get to 0xFF because we cant reach top of stack
        if self.stack_pointer != 0xFF:
            self.stack_pointer += 1
        self.pc += 2

    def PUSH(self, a, b):
        # move stack pointer down
        self.stack_pointer -= 1
        # get value from register
        val = self.reg[a]
        # insert value onto stack
        self.ram_write(self.stack_pointer, val)
        self.pc += 2

    def ADD(self, op_a, op_b):
        self.alu('ADD', op_a, op_b)
        self.pc += 3

    def JMP(self, a, b):
        # Set the `PC` to the address stored in the given register.
        self.pc = self.reg[a]

    def JEQ(self, a, b):
        if self.FLG == 0b00000001:
            self.pc = self.reg[a]
        else:
            self.pc += 2

    # populate branchtable

    def branch_operations(self):
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b10100111] = self.CMP
        self.branchtable[0b10100000] = self.ADD
        self.branchtable[0b01000110] = self.POP
        self.branchtable[0b01000101] = self.PUSH
        self.branchtable[0b01010000] = self.CALL
        self.branchtable[0b00010001] = self.RET

    # returns value at the address in memory
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
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] > self.reg[reg_b]:
                # modify sevent bit if a > b
                self.FLG = 0b00000010
            if self.reg[reg_a] < self.reg[reg_b]
            # modify sixth bit if b < a
            self.FLG = 0b00000100
            else:
                # modfy 8th bit if equal
                self.FLG = 0b00000001
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
            # store address of data
            cmd = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # halt cpu and exit emulator
            if cmd == HLT:
                print('closing run loop')
                running = False
                break

            elif cmd not in self.branchtable:
                print('unknown instruction')
                sys.exit(1)

            else:
                self.branchtable[cmd](operand_a, operand_b)
