"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        self.running = False
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""

        for address, instruction in enumerate(program):
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
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
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Read the memory address stored in register[pc]
        # Store result in 'IR', the instruction register (can be a local variable in run())

        branch_table = {
            self.LDI : self.ldi,
            self.MUL : self.mul,
            self.PRN : self.prn,
            self.HLT : self.hlt,
            self.PUSH: self.push,
            self.POP : self.pop
        }


        self.running = True
        self.reg[self.sp] = 0xF4
        print("R7: ", self.reg[self.sp])

        while self.running:
            ir = self.ram[self.pc]
            if ir in branch_table:
                branch_table[ir]()
            elif ir not in branch_table:
                print(f'Unknown instruction {bin(ir)} at address {self.pc}')
                sys.exit(1)
                

    def ldi(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[address] = value
        self.pc += 3

    def mul(self):
        reg_a = 0
        reg_b = 1
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3
    
    def push(self):
        self.reg[self.sp] -= 1
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        top_of_stack_addr = self.reg[self.sp]
        self.ram[top_of_stack_addr] = value
        self.pc += 2

    def pop(self):
        top_of_stack_address = self.reg[self.sp]
        reg_address = self.ram[self.pc + 1]
        self.reg[reg_address] = self.ram[top_of_stack_address]
        self.reg[self.sp] += 1
        self.pc += 2

    def prn(self):
        address = self.ram[self.pc + 1]
        value = self.reg[address]
        print("RAM: ", self.ram)
        print("REG: ", self.reg)
        print("Value", value)
        self.pc += 2

    def hlt(self):
        self.pc += 1
        self.running = False
