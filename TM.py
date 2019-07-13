from itertools import product
from time import sleep
# global variables:
halt = 'HALT' # the name of the final halt state
blank = ' ' # the blank symbol on the tape

class Tape:
	def __init__(self, tape_str):
		"""tape_str is a string representation of the tape state."""
		self.__state = dict(enumerate(tape_str))
		self.__head_pos = 0

	def __str__(self):
		"""Converts the tape into a string."""
		return "".join([self.__state[i] for i in sorted(self.__state)])

	def view(self):
		"""Prints the tape, pointer position included."""
		print(str(self) + '\n' + self.__head_pos * ' ' + '^', end='\r')

	def read(self):
		"""Reads the value at the head position."""
		return self.__state[self.__head_pos]

	def __move_head(self, i):
		"""
		Moves the tape head to by the specified amount. If the new head 
		position has not been occupied before, fills it with a blank character.
		"""
		self.__head_pos += i
		try: 
			self.__state[self.__head_pos]
		except KeyError:
			self.__state[self.__head_pos] = blank

	def right(self):
		"""Moves the tape head to the right."""
		self.__move_head(1)

	def left(self):
		"""Moves the tape head to the left."""
		self.__move_head(-1)

	def write(self, input):
		"""Writes the input at the head position."""
		self.__state[self.__head_pos] = input
		

class Case:
	def __init__(self, initState, readSym, writeSym, headMove, newState):
		"""
		The Case class contains one instruction for the tape head to carry out.
		A list of Cases makes up the TM's transition function.
		initState and readSym are identifiers, for the machine to choose which
		case to execute. writeSym, headMove, and newState are the actions the
		TM will take if this case is executed.
		initState: The initial state of the TM
		readSym: The current symbol at the tape head.
		writeSym: The symbol that the tape head should write to the tape.
		headMove: Whether the tape head should move right (True) or left (False).
		newState: The state the TM moves to after execution.
		"""
		self.initState = initState
		self.readSym = readSym
		self.writeSym = writeSym
		self.headMove = headMove
		self.newState = newState


class Machine:
	def __init__(self, stateSet, alphabet, initState, transFunc):
		"""
		stateSet: A list of possible states for the TM to take.
		alphabet: A list of possible symbols to appear on the tape.
		initState: The state the TM starts in.
		transFunc: A list of Case objects that govern how the TM modifies the tape.
		"""
		alphabet += [blank]
		if initState not in stateSet:
			raise ValueError("Initial state not in set of possible states.")

		suppliedCases = [(x.initState, x.readSym) for x in transFunc]
		if len(set(suppliedCases)) != len(suppliedCases):
			raise ValueError("Two Case objects provided for one case-symbol combination.")
		allPerms = list(product(stateSet, alphabet))
		missingCases = [case for case in allPerms if case not in suppliedCases]
		if len(missingCases) != 0:
			print("Cases not provided for every possible combination of states "
				  "and symbols. Unsupplied cases are assumed to lead to a halt.")
			for case in missingCases:
				transFunc += [Case(case[0], case[1], case[1], True, halt)]
		impossibleCases = [case for case in suppliedCases if case not in allPerms]
		if len(impossibleCases) != 0:
			print("Warning: Cases supplied that contain states or symbols "
				  "not in the TM's alphabet. These cases will have no effect "
				  "on the execution of the program.")

		self.stateSet = stateSet
		self.alphabet = alphabet
		self.initState = initState
		self.transFunc = transFunc


	def eval(self, tape, view=True, interval=.1):
		"""
		Takes a Tape object and executes a series of instructions provided
		by the Machine's transition function. This is the actual "Turing 
		machine" evaluation. The view parameter, if True, prints the tape as
		the Machine operates. If False, only prints the tape after the machine
		halts. The interval parameter determines how long each step of
		execution takes.
		"""
		for c in str(tape):
			if c not in self.alphabet:
				raise ValueError("Invalid symbol in tape.")
		state = self.initState
		if view:
			tape.view()
		while state != halt:
			currentRead = tape.read()
			for case in self.transFunc:
				if case.initState == state and case.readSym == currentRead:
					opCase = case
					break
			tape.write(opCase.writeSym)
			if opCase.headMove:
				tape.right()
			else:
				tape.left()
			state = opCase.newState
			if view:
				tape.view()
			sleep(interval)


# Example: Binary palindrome detector. If the tape is blank when the program
# halts, the string is a palindrome. Otherwise, the string is not a
# palindrome.
delta = [Case('i', blank, blank, True, halt),
		 Case('i', '0', blank, True, 'p0'),
		 Case('i', '1', blank, True, 'p1'),
		 Case('p0', '0', '0', True, 'p0'),
		 Case('p0', '1', '1', True, 'p0'),
		 Case('p1', '0', '0', True, 'p1'),
		 Case('p1', '1', '1', True, 'p1'),
		 Case('p0', blank, blank, False, 'q0'),
		 Case('p1', blank, blank, False, 'q1'),
		 Case('q0', '0', blank, False, 'r'),
		 Case('q1', '1', blank, False, 'r'),
		 Case('q0', blank, blank, True, halt),
		 Case('q1', blank, blank, True, halt),
		 Case('r', '0', '0', False, 'r'),
		 Case('r', '1', '1', False, 'r'),
		 Case('r', blank, blank, True, 'i')
		 ]
TM = Machine(stateSet=['i', 'p0', 'p1', 'q0', 'q1', 'r'],
			 alphabet=['0', '1'],
			 initState='i',
			 transFunc=delta)

tape1 = Tape("10101")
TM.eval(tape1)
print("*"*80)
tape2 = Tape("1101")
TM.eval(tape2)

input("Press enter to exit")
