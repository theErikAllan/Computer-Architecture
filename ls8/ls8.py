#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

program = []

if len(sys.argv) < 2:
    print("GIVE ME A BETTER FILE. YOU'RE USELESS.")
    exit()

filepath = sys.argv[1]

with open(filepath) as banana:
    for line in banana:
        if line[0] != "#":
            line = line.rstrip()
            if line != '':
                num = int(line[0:8], 2)
                # print(num)
                program.append(num)


cpu = CPU()

cpu.load(program)
cpu.run()