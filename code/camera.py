#! usr/bin/env python
# Camera class definition
# This class allows the world to scroll without having to move the object's positions around in the physics engine every frame.
# It does this by creating a Chipmunk object that is jointed to the player's position.
# If any Chipmunk objects are colliding with the Camera, they are drawn because they are in the "visible" space
from pymunk import Vec2d
from constants import *
class Camera():
	def __init__(self, link=None):
		self.position = Vec2d(0, 0)
		self.link = link
		return
	def update(self):
		self.position = self.link.position
		return
	def setLink(self, link):
		self.link = link
		return
	def findPosition(self, posOfObject):
		if self.link != None:
			if self.position.x > posOfObject.x:
				return Vec2d(posOfObject.x, posOfObject.y)
			if self.position.x < posOfObject.x:
				return Vec2d(posOfObject.x, posOfObject.y)
			else:
				return posOfObject
		else:
			return posOfObject
