# Connect-Four

Python program uses Tkinter GUI to implement a fully functional Connect-Four game. User plays against AI, which learns from previous outcomes and uses clustering heuristics to make informed decisions. AI trains against itself for rapid learning.

**Main.py** - Instantiates the Connect-4 Class, contains game loop logic, drawing functions, and driver functions.  
**Nodes.py** - Each object of the Nodes class represents a "square" on the gameboard. Has x,y coordinates and a dictionary of pointers to its neighbors.  
**AI.py** - Responsible for evaluating the current state of the gameboard, AI decision making, and reading in/writing to csv files.  
