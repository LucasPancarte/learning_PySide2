from contextlib import contextmanager


class SimpleClassWithContext():
	"""
	Over explained class to show the use of contextmanager
	"""

	# make a class variable
	do_something = False

	@classmethod
	@contextmanager
	def do_something_context(cls):
		"""
		A context that temporarly forces a value on the class variable
		This is a simple exemple be but we can write more complexe code
		before and after the 'yield' keyword.
		The 'yield' keyword in this context executes the code found inside
		the 'with' keyword block.
		The order of execution is as follows: <code before yield> -> <code in the with block> -> <code after yield>

		"""
		temp_value = cls.do_something
		cls.do_something = True 
		yield 
		cls.do_something = temp_value

	def __init__(self):
		"""
		Init class
		"""
		self.force_do_something()

	def force_do_something(self):
		"""
		We can see the 'do_something' variable changing inside the 'with' keyword block
		and returning to it s original state once the block is finished
		"""
		print("Should I do something : {}".format(self.do_something))

		with self.do_something_context():
			print("I am forced to do something : {}".format(self.do_something))

		print("Should I do something after being forced : {}".format(self.do_something))


if __name__ == "__main__":

	simp_context_class = SimpleClassWithContext()