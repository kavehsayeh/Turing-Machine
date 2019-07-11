class Tape:
	def __init__(self, tape_str):
		"""tape_str is a string representation of the tape state."""
		self.__state = dict(enumerate(tape_str))
		self.__head_pos = 0

	def __str__(self):
		"""Converts the tape into a string."""
		return "".join([self.__state[i] for i in sorted(self.__state)])

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
			self.__state[self.__head_pos] = ' '

	def right(self):
		"""Moves the tape head to the right."""
		self.__move_head(1)

	def left(self):
		"""Moves the tape head to the right."""
		self.__move_head(-1)

	def write(self, input):
		"""Writes the input at the head position."""
		self.__state[self.__head_pos] = input


tape = Tape("1001")
tape.left()
tape.left()
tape.write("1")
tape.right()
tape.write("b")
print(str(tape))
