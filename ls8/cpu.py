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
        self.running = False
        self.ADD  = 0b10100000
        self.CALL = 0b01010000
        self.LDI  = 0b10000010
        self.PRN  = 0b01000111
        self.HLT  = 0b00000001
        self.MUL  = 0b10100010
        self.PUSH = 0b01000101
        self.POP  = 0b01000110
        self.RET  = 0b00010001

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
        self.running = True
        # First, we set the stack pointer in the register to point to address F3 in ram, which is reserved for the start of the stack
        self.reg[self.sp] = 0xF3

        branch_table = {
            self.ADD  : self.add,
            self.CALL : self.call,
            self.LDI  : self.ldi,
            self.PRN  : self.prn,
            self.HLT  : self.hlt,
            self.MUL  : self.mul,
            self.PUSH : self.push,
            self.POP  : self.pop,
            self.RET  : self.ret
        }

        while self.running:
            # We retrieve the program instruction from ram
            instruction_register = self.ram_read(self.pc)
            # Next, we check if the instruction register is in our branch table and execute it if it is
            if instruction_register in branch_table:
                branch_table[instruction_register]()
            elif instruction_register not in branch_table:
                print("REG: ", self.reg)
                print("RAM: ", self.ram)
                print(f'Unknown instruction {bin(instruction_register)} at address {self.pc}')
                sys.exit(1)
    
    def add(self):
        # Add the values in regA and regB
        regA = self.ram_read(self.pc + 1)
        regB = self.ram_read(self.pc + 2)
        self.alu("ADD", regA, regB)
        self.pc += 3
    
    def call(self):
        # Calls a subroutine at the specified register address
        # The address of next instruction after CALL (self.pc + 2) is pushed to the top of the stack
        next_IR = self.pc + 2
        self.reg[self.sp] -= 1
        top_of_stack_address = self.reg[self.sp]
        self.ram_write(top_of_stack_address, next_IR)

        # Pushing the address of the next instruction allows us to return to where we left off when the subroutine finishes executing
        
        # The program counter is set to the address stored in the given register
        reg_address = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_address]

    def hlt(self):
        self.pc += 1
        self.running = False

    def ldi(self):
        # First, we grab the register address that we'll be storing a value in
        reg_address = self.ram_read(self.pc + 1)
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
    
    def pop(self):
        # Pop the value at the top of the stack into the given register
        # Copy the value from the address pointed to by the stack pointer and into the given register
        top_of_stack_address = self.reg[self.sp]
        value = self.ram_read(top_of_stack_address)
        reg_address = self.ram_read(self.pc + 1)
        self.reg[reg_address] = value
        # Increment the stack pointer to account for popping off the top of the stack
        self.reg[self.sp] += 1
        self.pc += 2

    def prn(self):
        # Print numeric value stored in the given register
        # First, we get the register address from ram
        reg_address = self.ram_read(self.pc + 1)
        # Then we access the register address and print the value contained within
        value = self.reg[reg_address]
        print("PRINTED VALUE: ", value)
        self.pc += 2

    def push(self):
        # Push the value from the given register to the stack
        # Decrement the stack pointer
        self.reg[self.sp] -= 1
        # Copy the value from the given register to the address pointed to by the stack pointer
        reg_address = self.ram_read(self.pc + 1)
        value = self.reg[reg_address]
        top_of_stack_address = self.reg[self.sp]
        self.ram_write(top_of_stack_address, value)
        self.pc += 2
    
    def ret(self):
        # Pop the value from the top of the stack and point the program counter at it
        # Pop the value at the top of the stack into the given register
        # Copy the value from the address pointed to by the stack pointer and into the given register
        top_of_stack_address = self.reg[self.sp]
        pc_to_return_to = self.ram_read(top_of_stack_address)
        # Increment the stack pointer to account for popping off the top of the stack
        self.reg[self.sp] += 1
        self.pc = pc_to_return_to