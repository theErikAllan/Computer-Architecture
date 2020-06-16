"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, program):
        """Load a program into memory."""


        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

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
        running = True

        while running:
            instruction_register = self.ram[self.pc]
            
            if instruction_register == self.LDI:
                self.ldi()
            
            elif instruction_register == self.MUL:
                self.mul()

            elif instruction_register == self.PRN:
                self.prn()

            elif instruction_register == self.HLT:
                running = self.hlt()

            else: 
                print(f'Unknown instructions {ir} at address {self.pc}')
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

    def prn(self):
        address = self.ram[self.pc + 1]
        print("RAM: ", self.ram)
        print("REG: ", self.reg)
        print(self.reg[address])
        self.pc += 2

    def hlt(self):
        self.pc += 1
        return False
