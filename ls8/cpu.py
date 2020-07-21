"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256
        self.reg = [None] * 8
        self.pc = 0
        self.sp = 7
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op =="MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this from run() if you need help debugging.
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
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        running = True
        # First, we set the stack pointer in the register to point to address F3 in ram, which is reserved for the start of the stack
        self.reg[self.sp] = 0xF3

        while running:
            # We retrieve the program instruction from ram
            instruction_register = self.ram[self.pc]
            # Next, we create a list of conditionals checking if the program or space assigned to program
            if instruction_register == self.LDI:
                self.ldi()
            elif instruction_register == self.PRN:
                self.prn()
            elif instruction_register == self.HLT:
                running = self.hlt()
            elif instruction_register == self.MUL:
                self.mul()

    def ldi(self):
        # First, we grab the register address that we'll be storing a value in
        reg_address = self.ram[self.pc + 1]
        # Then we grab the value
        value = self.ram_read(self.pc + 2)
        # And store the value in the designated register
        self.reg[reg_address] = value
        # Lastly, we increment the program counter so it moves on to the next instruction
        self.pc += 3

    def mul(self):
        # Multiply the values in regA and regB
        regA = self.ram_read(self.pc + 1)
        regB = self.ram_read(self.pc + 2)
        self.alu("MUL", regA, regB)
        self.pc += 3

    def prn(self):
        # Print numeric value stored in the given register
        # First, we get the register address from ram
        reg_address = self.ram[self.pc + 1]
        # Then we access the register address and print the value contained within
        value = self.reg[reg_address]
        print(value)
        self.pc += 2

    def hlt(self):
        self.pc += 1
        return False