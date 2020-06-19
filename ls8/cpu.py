"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

        # PC: Program Counter, address of the currently executing instruction
        self.pc = 0
        self.sp = 7
        self.running = False

        # The flags register `FL` holds the current flags status. These flags can change based on the operands given to the `CMP` opcode.
        self.fl = 0b00000000

        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.ADD = 0b10100000
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.CMP = 0b10100111
        self.JNE = 0b01010110
        self.JEQ = 0b01010101
        self.JMP = 0b01010100
    
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
        # We write a conditional statement for CMP
        elif op == "CMP":
            # And in the statement we check the flag
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000001
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
            self.ADD : self.add,
            self.MUL : self.mul,
            self.PRN : self.prn,
            self.HLT : self.hlt,
            self.PUSH: self.push,
            self.POP : self.pop,
            self.CALL: self.call,
            self.RET : self.ret,
            self.CMP : self.comp,
            self.JEQ : self.jeq,
            self.JNE : self.jne,
            self.JMP : self.jmp
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
        # print("State of RAM: ", self.ram)
        self.pc += 3

    def comp(self):
        reg_a = 0
        reg_b = 1
        self.alu("CMP", reg_a, reg_b)
        self.pc += 3
    
    def add(self):
        reg_a = 0
        reg_b = 0
        self.alu("ADD", reg_a, reg_b)
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

    def call(self):
        # Calls a subroutine at the address stored in the register

        # First, we create a variable and point it to (self.pc + 2), which represents the place in the program where we want to return to after our subroutine is executed
        return_pc = self.pc + 2

        # Then we decrement the stack pointer in R7 to the new head of the stack
        self.reg[self.sp] -= 1
        # We create a variable and point it to the value in R7 to represent the address in RAM of the top of the stack
        top_of_stack_address = self.reg[self.sp]
        # And then we storeat the top of the stack the PC value we want to return to 
        self.ram[top_of_stack_address] = return_pc

        # Next, we create a variable for the register address of the subroutine we want to run 
        reg_address_of_subroutine = self.ram[self.pc + 1]
        # We create another variable and point it to the register address containing the PC of the subroutine we want to run
        subroutine_pc = self.reg[reg_address_of_subroutine]
        # Finally, we set self.pc to point to the PC of the subroutine we want to run so the computer will jump to that location in the program
        self.pc = subroutine_pc
    
    def ret(self):
        # Return from subroutine
        # Pop the value from the top of the stack and store it in the PC
        print("REG: ", self.reg)
        top_of_stack_address = self.reg[self.sp]
        return_pc = self.ram[top_of_stack_address]
        self.pc = return_pc

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

    def jmp(self):
        # Jump to the address stored in the given register
        reg_address = self.ram[self.pc + 1]
        self.pc = self.reg[reg_address]

    def jeq(self):
        if self.fl == 1:
            reg_address = self.ram[self.pc + 1]
            self.pc = self.reg[reg_address]
        else:
            self.pc += 2

    def jne(self):
        if self.fl != 1:
            reg_address = self.ram[self.pc + 1]
            self.pc = self.reg[reg_address]
        else:
            self.pc += 2
