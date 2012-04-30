#! usr/bin/env python
# All Object child definitions
import pygame
import random
from constants import *
from createshapes import *
from pymunk import Vec2d, SlideJoint
import math

# Definitions
# The generic Object type. Don't create instances of this directly
class Object(pygame.sprite.Sprite):
	def __init__(self, world, position):
		pygame.sprite.Sprite.__init__(self)
		world.addObject(self)
		return
	def update(self, world):
		self.Draw(world)
		return
	def Draw(self, world):
		return

# A simple block that you can stand on. Does not have to be a square.
# Pass it a world and position
# Optional arguments: size(width, height) static, mass, friction, elasticity, collision type
class Block(Object):
	def __init__(self, world, position, size, static=True, collision=GROUNDCOLLISIONTYPE, mass=20, friction=0.5, elasticity=0.2):
		global GROUNDCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.shape = createBox(position, self.size, mass, friction, elasticity, static)
		self.shape.collision_type = collision
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
		return
	def Draw(self, world):
		pygame.draw.polygon(world.screen, (50, 255, 50), self.shape.get_points())
		pygame.draw.polygon(world.screen, (10, 10, 10), self.shape.get_points(), 4)
		return

# A simple convex polygon that you can stand on.
# Pass it a world, position, and some vertices (given in local coordinates from the position
# Optional arguments: static, mass, friction, elasticity, collision type
class Poly(Object):
	def __init__(self, world, position, vertices, static=True, collision=GROUNDCOLLISIONTYPE, mass=20, friction=0.5, elasticity=0.5):
		global GROUNDCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.vertices = vertices
		self.shape = createPolygon(position, vertices, mass, friction, elasticity, static)
		self.shape.collision_type = collision
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
		return
	def Draw(self, world):
		pygame.draw.polygon(world.screen, (50, 255, 50), self.shape.get_points())
		pygame.draw.polygon(world.screen, (0, 0, 0), self.shape.get_points(), 4)
		return

# A circle
# Pass it a world, position, and radius
# Optional arguments: mass, friction, elasticity, collision type
class Circle(Object):
	def __init__(self, world, position, radius, static=True, collision=GROUNDCOLLISIONTYPE, mass=20, friction=0.5, elasticity=0.5):
		global GROUNDCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.shape = createBall(position, radius, mass, friction, elasticity, static)
		self.shape.collision_type = collision
		world.addObject(self)
		if not static:
			world.space.add(self.shape.body, self.shape)
		else:
			world.space.add_static(self.shape)
		return
	def Draw(self, world):
		pygame.draw.circle(world.screen, (50, 255, 50), self.shape.body.position.int_tuple, int(self.shape.radius))
		pygame.draw.circle(world.screen, (0, 0, 0), self.shape.body.position.int_tuple, int(self.shape.radius), 4)
		return

# A dynamic rope that the player can swing on.
class Rope(Object):
	def __init__(self, world, position, length, mass=20, friction=0.4, elasticity=0.1):
		pygame.sprite.Sprite.__init__(self)
		self.shapes = []
		self.setupLinks(world, position, length, mass, friction, elasticity)
		world.addObject(self)
	def Draw(self, world):
		for shape in self.shapes:
			pygame.draw.circle(world.screen, (255, 170, 50), shape.body.position.int_tuple, int(shape.radius))
			pygame.draw.circle(world.screen, (0, 0, 0), shape.body.position.int_tuple, int(shape.radius), 4)
		return
	def setupLinks(self, world, position, length, mass, friction, elasticity):
		global ROPESIZE
		nextpos = [position[0], position[1]]
		anchor = createBall(nextpos, ROPESIZE, mass, friction, elasticity, True)
		world.space.add_static(anchor)
		self.shapes.append(anchor)
		for i in range(length*ROPESTIFFNESS, ROPESTIFFNESS, -ROPESTIFFNESS/10):
			nextpos[1] += ROPESIZE*2.1
			link = createBall(nextpos, ROPESIZE, i, friction, elasticity, False)
			world.space.add(link.body, link)
			joint = SlideJoint(self.shapes[-1].body, link.body, (0, 0), (0, 0), 0, ROPESIZE*2.1)
			world.space.add(joint)
			self.shapes.append(link)
		self.shapes[-1].collision_type = ROPECOLLISIONTYPE
		return


# A piece of text that can be placed anywhere.
# pass it a world and position and text
# Optional arguments include: color, size, boldness
class Text(Object):
	def __init__(self, world, position, text, color=(255, 255, 255), size=16, boldness=False):
		self.font = pygame.font.Font(None, size)
		self.font.set_bold(boldness)
		self.image = self.font.render(text, True, color)
		self.position = position
		world.addObject(self)
	def Draw(self, world):
		world.screen.blit(self.image, self.position)
		return

# A box that is painted red. And kills climbers
# Can be static or not
class DeathBox(Object):
	def __init__(self, world, position, size, static=True):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.shape = createBox(position, self.size, 1, 0.0, 0.0, static)
		self.shape.collision_type = DEATHCOLLISIONTYPE
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
	def Draw(self, world):
		pygame.draw.polygon(world.screen, (250, 200, 200), self.shape.get_points())
		pygame.draw.polygon(world.screen, (100, 50, 50), self.shape.get_points(), 4)
		return

# An object that is extremely bouncy
# Pass it a world and position
# Optional arguments: static
class Spring(Object):
	def __init__(self, world, position, static=True):
		pygame.sprite.Sprite.__init__(self)
		self.size = (40, 10)
		self.shape = createBox(position, self.size, 1, 0.0, 3, static)
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
	def Draw(self, world):
		pygame.draw.polygon(world.screen, (255, 100, 100), self.shape.get_points())
		pygame.draw.polygon(world.screen, (50, 230, 90), self.shape.get_points(), 4)
		return

# The thing the player is trying to touch
# Pass it a world and position
# When the player touches it the world.PlayerTouchedGoal method is called.
class Goal(Object):
	def __init__(self, world, position):
		global GOALCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.size = (20, 10)
		self.shape = createBox(position, self.size)
		self.shape.collision_type = GOALCOLLISIONTYPE
		world.addObject(self)
		world.space.add(self.shape.body, self.shape)
		return
	def Draw(self, world):
		pygame.draw.polygon(world.screen, (255, 255, 0), self.shape.get_points())
		pygame.draw.polygon(world.screen, (200, 200, 200), self.shape.get_points(), 4)
		return
