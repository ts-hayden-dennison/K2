#! usr/bin/env python
# Run this file to play the game.

from code import K2
from sys import argv
if len(argv) > 1:
	if '-leveleditor' in argv:
		from code import leveleditor
		leveleditor.main()

# Here we go!
K2.main()
