#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

program = []
file_name = sys.argv[1]
print("File: ", file_name)

with open(file_name) as f:
    lines = f.readlines()
    for line in lines:
        if line[0]!='#':
            num = int(line[0:8], 2)
            program.append(num)

cpu = CPU()

cpu.load(program)
cpu.run()
# cpu.mult()