#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

if len(sys.argv) != 2:
    print('must have filename')
    sys.exit(1)

cpu.load(sys.argv)
cpu.run()
