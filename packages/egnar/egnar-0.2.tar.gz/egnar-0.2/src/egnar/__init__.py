import typing
import decimal
import fractions

class egnar:
	@typing.overload
	def __init__(self, end) -> None: ...
	@typing.overload
	def __init__(self, start, end, step = 1) -> None: ...
	def __init__(self, start, end, step = 1) -> None:
		if step == 0:
			raise ValueError(f"{self.__rangename__}() arg 3 must not be zero")
		self.current = self.T(start)
		self.start = self.T(start)
		self.end = self.T(end)
		self.step = self.T(step)
		self.len = len([x for x in self])

	def __iter__(self) -> typing.Iterator[typing.Any]:
		return self

	def __next__(self) -> typing.Any:
		return_value: self.T = self.current
		condition: bool = self.current < self.end if self.step > 0 else self.current > self.end
		if condition:
			self.current += self.step
		else:
			self.current = self.start
			raise StopIteration
		return return_value

	def __repr__(self) -> str:
		return f"{self.__rangename__}({self.start}, {self.end}, {self.step})"
	
	def __len__(self) -> int:
		return self.len
	
	@typing.overload
	def __getitem__(self, index: typing.SupportsIndex) -> int: ...
	@typing.overload
	def __getitem__(self, slice_data: slice) -> typing.Self: ...
	def __getitem__(self, value: typing.Any):
		tp = type(value)
		if tp != int | tp != slice:
			raise TypeError(f"{self.__rangename__} indices must be integers or slices, not {tp.__name__}")
		result = list(self)[value]
		if tp == slice:
			result = self.__class__(result[0], result[-1] + self.step, self.step)
		return result
	
	def __reversed__(self) -> typing.Self:
		return self.__class__(self.end - self.step, self.start - self.step, -self.step)
	
	def __eq__(self, other: typing.Self) -> bool:
		if type(other) != type(self):
			return False
		self_list = list(self)
		other_list = list(other)
		return self_list == other_list
	
	def __ne__(self, other: typing.Self) -> bool:
		return not self == other
	
	def index(self, value) -> int:
		for index, i in enumerate(self):
			if value == i:
				return index
		raise ValueError(f"{value} is not in {self.__rangename__}")

	def count(self, value) -> int:
		for i in self:
			if value == i:
				return 1
		return 0
	
	@property
	def __rangename__(self) -> str:
		return f"{self.__class__.__name__}"

class frange(egnar):
	T = float

class drange(egnar):
	T = decimal.Decimal

class farange(egnar):
	T = fractions.Fraction