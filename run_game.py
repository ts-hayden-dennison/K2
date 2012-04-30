#! usr/bin/env python
# Run this file to play the game.

from code import K2
from sys import argv
if len(argv) > 1:
	if argv[1] == '-leveleditor':
		from code import leveleditor
# Here we go!
K2.main()
