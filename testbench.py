class Classy_the_classy_class:#(object):
	"""docstring for Classy_the_classy_class"""
	def __init__(self, num1:int, num2:int):
		#super(Classy_the_classy_class, self).__init__()
		self.num1 = num1
		self.num2 = num2
	def thing(self):
		print(self.combined)
	@property
	def combined(self):
			return self.num1 + self.num2

classic = Classy_the_classy_class(1,3)
classic.thing()
print(classic.num1,classic.num2,classic.combined)
classic.num2 = 1

print(classic.num1,classic.num2,classic.combined)