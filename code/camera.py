#! usr/bin/env python
# Camera class definition
from pymunk import Vec2d
from util import *
import os

class Camera():
	def __init__(self):
		self.moved = Vec2d()
		self.loadBackgrounds()
		return
	def loadBackgrounds(self):
		self.backgrounds = []
		for image in os.listdir(os.path.join(os.path.join(os.getcwd(), IMAGEFOLDER), '1')):
			self.backgrounds.append(imgload(os.path.join(os.path.join(os.path.join(os.getcwd(), IMAGEFOLDER), '1'), image)))
		return
	def findPos(self, point):
		diff = point-self.moved
		return diff.int_tuple
	def move(self, delta):
		self.moved += delta
		return
