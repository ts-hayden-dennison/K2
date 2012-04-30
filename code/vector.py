#! usr/bin/env python
import math
class Vector():
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y
	def __str__(self):
		return '(%s, %s)' % (self.x, self.y)
	def __add__(self, rhs):
		return Vector(self.x + rhs.x, self.y + rhs.y)
	def __sub__(self, rhs):
		return Vector(self.x - rhs.x, self.y - rhs.y)
	def __mul__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar)
	def __neg__(self):
		return Vector(-self.x, -self.y)
	def __div__(self, scalar):
		return Vector(self.x/scalar, self.y/scalar)
	@classmethod
	def from_points(klass, p1, p2):
		return klass(p2[0] - p1[0], p2[1] - p1[1])
	@classmethod
	def from_tuple(klass, t):
		return Vector(t[0], t[1])
	def get_mag(self):
		return math.sqrt(self.x**2 + self.y**2)
	def normalize(self):
		mag = self.get_mag()
		try:
			self.x /= mag
			self.y /= mag
		except:
			self.x = 0
			self.y = 0
	def get_normalized(self):
		mag = self.get_mag()
		return Vector(self.x/mag, self.y/mag)
	def get_int(self):
		return Vector(int(self.x), int(self.y))
	def __iter__(self):
		return iter([self.x, self.y])
	def int_tuple(self):
		return (int(self.x), int(self.y))
