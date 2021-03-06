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

# An NPC. What did you think?
class NPC(Object):
	def __init__(self, world, position):
		pygame.sprite.Sprite.__init__(self)
		self.shape = createBall(position, ENEMYSIZE, 20, 0.5, 0.5, False)
		self.shape.collision_type = ROPECOLLISIONTYPE
		world.addObject(self)
		world.space.add(self.shape.body, self.shape)
		self.direction = -1
	def update(self, world):
		self.shape.body.apply_impulse(Vec2d(ENEMYSPEED*self.direction, 0))
		if abs(self.shape.body.velocity.x) > ENEMYSPEED*3:
			self.shape.body.velocity.x = self.direction*ENEMYSPEED
		bb = self.shape.cache_bb()
		if self.direction == -1:
			shapes = world.space.point_query((bb.left, bb.bottom))
		else:
			shapes = world.space.point_query((bb.right, bb.bottom))
		if len(shapes) > 0:
			self.direction *= -1
		self.Draw(world)
		return
	def Draw(self, world):
		newimg = pygame.transform.rotate(world.getImage('npc'), self.shape.body.angle*-180/3.14)
		newimg.convert()
		newimg.set_alpha(230)
		position = world.camera.findPos(self.shape.body.position)
		world.screen.blit(newimg, (position-Vec2d(newimg.get_width()/2, newimg.get_height()/2)))
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

# A simple convex polygon that you can stand on.
# Pass it a world, position, and some vertices (given in local coordinates from the position
# Optional arguments: static, mass, friction, elasticity, collision type
class GroundPoly(Object):
	def __init__(self, world, position, vertices, static=True, mass=20, friction=0.5, elasticity=0.5):
		global GROUNDCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.vertices = vertices
		self.shape = createPolygon(position, vertices, mass, friction, elasticity, static)
		self.shape.collision_type = GROUNDCOLLISIONTYPE
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
		return
	def Draw(self, world):
		points = self.shape.get_points()
		for p in points:
			points[points.index(p)] = world.camera.findPos(p)
		pygame.draw.polygon(world.screen, (0, 255, 10), points, random.choice((0, 0, 0, 0, 0, 0, 0, 2, 3, 4)))
		return

class DeathPoly(Object):
	def __init__(self, world, position, vertices, static=True, mass=20, friction=0.5, elasticity=0.5):
		global DEATHCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.vertices = vertices
		self.shape = createPolygon(position, vertices, mass, friction, elasticity, static)
		self.shape.collision_type = DEATHCOLLISIONTYPE
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
		return
	def Draw(self, world):
		points = self.shape.get_points()
		for p in points:
			points[points.index(p)] = world.camera.findPos(p)
		pygame.draw.polygon(world.screen, (255, 255, 255), points)
		pygame.draw.polygon(world.screen, (255, 0, 0), points, 2)
		return

class ClingPoly(Object):
	def __init__(self, world, position, vertices, static=True, mass=20, friction=0.5, elasticity=0.5):
		global ROPECOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.vertices = vertices
		self.shape = createPolygon(position, vertices, mass, friction, elasticity, static)
		self.shape.collision_type = ROPECOLLISIONTYPE
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
		return
	def Draw(self, world):
		points = self.shape.get_points()
		for p in points:
			points[points.index(p)] = world.camera.findPos(p)
		pygame.draw.polygon(world.screen, (255, 255, 255), points)
		pygame.draw.polygon(world.screen, (255, 0, 0), points, 2)
		return

class AlivePoly(Object):
	def __init__(self, world, position, vertices, static=False, mass=20, friction=0.5, elasticity=0.5):
		global PLAYERCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.vertices = vertices
		self.shape = createPolygon(position, vertices, mass, friction, elasticity, static)
		self.shape.collision_type = PLAYERCOLLISIONTYPE
		world.addObject(self)
		if static == True:
			world.space.add_static(self.shape)
		else:
			world.space.add(self.shape.body, self.shape)
		return
	def Draw(self, world):
		points = self.shape.get_points()
		for p in points:
			points[points.index(p)] = world.camera.findPos(p)
		pygame.draw.polygon(world.screen, (255, 255, 255), points)
		pygame.draw.polygon(world.screen, (255, 0, 0), points, 2)
		return

# A circle
# Pass it a world, position, and radius
# Optional arguments: mass, friction, elasticity, collision type
class GroundCircle(Object):
	def __init__(self, world, position, radius, static=True, mass=20, friction=0.5, elasticity=0.5):
		global GROUNDCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.shape = createBall(position, radius, mass, friction, elasticity, static)
		self.shape.collision_type = GROUNDCOLLISIONTYPE
		world.addObject(self)
		if not static:
			world.space.add(self.shape.body, self.shape)
		else:
			world.space.add_static(self.shape)
		return

class DeathCircle(Object):
	def __init__(self, world, position, radius, static=True, mass=20, friction=0.5, elasticity=0.5):
		global DEATHCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.shape = createBall(position, radius, mass, friction, elasticity, static)
		self.shape.collision_type = DEATHCOLLISIONTYPE
		world.addObject(self)
		if not static:
			world.space.add(self.shape.body, self.shape)
		else:
			world.space.add_static(self.shape)
		return

class ClingCircle(Object):
	def __init__(self, world, position, radius, static=True, mass=20, friction=0.5, elasticity=0.5):
		global ROPECOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.shape = createBall(position, radius, mass, friction, elasticity, static)
		self.shape.collision_type = ROPECOLLISIONTYPE
		world.addObject(self)
		if not static:
			world.space.add(self.shape.body, self.shape)
		else:
			world.space.add_static(self.shape)
		return

class AliveCircle(Object):
	def __init__(self, world, position, radius, static=False, mass=20, friction=0.5, elasticity=0.5):
		global PLAYERCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.shape = createBall(position, radius, mass, friction, elasticity, static)
		self.shape.collision_type = PLAYERCOLLISIONTYPE
		world.addObject(self)
		if not static:
			world.space.add(self.shape.body, self.shape)
		else:
			world.space.add_static(self.shape)
		return

# A dynamic rope that the player can swing on.
class Rope(Object):
	def __init__(self, world, position, length, mass=20, friction=0.4, elasticity=0.1):
		pygame.sprite.Sprite.__init__(self)
		self.length = length
		self.shapes = []
		self.setupLinks(world, position, length, mass, friction, elasticity)
		world.addObject(self)
	def Draw(self, world):
		for shape in self.shapes:
			pygame.draw.circle(world.screen, (255, 170, 50), world.camera.findPos(shape.body.position).int_tuple, int(shape.radius))
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
