import typing
import decimal
import fractions

class range_base:
	@typing.overload
	def __init__(self, end) -> None: ...
	@typing.overload
	def __init__(self, start, end, step = 1) -> None: ...
	def __init__(self, start, end, step = 1) -> None:
		if step == 0:
			raise ValueError(f"{self.__class__.__name__}() arg 3 must not be zero")
		self.current = self.T(start)
		self.start = self.T(start)
		self.end = self.T(end)
		self.step = self.T(step)

	def __iter__(self):
		return self

	def __next__(self):
		return_value: self.T = self.current
		condition: bool = self.current < self.end if self.step > 0 else self.current > self.end
		if condition:
			self.current += self.step
		else:
			raise StopIteration
		return return_value
	
class frange(range_base):
	T = float

class drange(range_base):
	T = decimal.Decimal

class farange(range_base):
	T = fractions.Fraction