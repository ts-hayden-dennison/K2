#! usr/bin/env python
# The object definition for the Climber class (player-controlled)
import pygame
from objects import Object
from constants import *
from createshapes import createBall
from sys import exit
from pymunk import Vec2d, SlideJoint

# The player-controlled thing
# Pass it a world and position
# Optional arguments: collision type, size
class Climber(Object):
	def __init__(self, world, position, collision=PLAYERCOLLISIONTYPE, size=PLAYERSIZE):
		global PLAYERMASS, PLAYERFRICTION, PLAYERBOUNCE, PLAYERCOLLISIONTYPE, ACTIONLENGTH, GROUNDCOLLISIONTYPE
		pygame.sprite.Sprite.__init__(self)
		self.canJump = False
		self.canLengthenJump = False
		self.jumpLengthen = 1
		self.actionTimer = ACTIONLENGTH
		self.shape = createBall(position, PLAYERSIZE, PLAYERMASS, PLAYERFRICTION, PLAYERBOUNCE)
		self.shape.collision_type = collision
		self.death = False
		self.setupCollisionHandlers(world)
		self.ropejoint = None
		self.screenPosition = Vec2d(WIDTH/2, HEIGHT/2)
		world.addObject(self)
		world.space.add(self.shape.body, self.shape)
		world.camera.setup(self.shape.body.position)
		return
	def getDeath():
		return self.death
	def update(self, world):
		self.decreaseActionTimer()
		self.Draw(world)
		self.Do(world)
		self.checkIfTouchingShapes(world)
		return
	def checkIfTouchingShapes(self, world):
		shapes = world.space.shape_query(self.shape)
		if len(shapes) == 0:
			self.canJump = False
		for shape in shapes:
			if shape.collision_type == ROPECOLLISIONTYPE:
				if self.ropejoint == None:
					self.ropejoint = SlideJoint(self.shape.body, shape.body, (0, 0), (0, 0), PLAYERSIZE+2, PLAYERSIZE+5)
					world.space.add(self.ropejoint)
					break
				else:
					self.removeJoints(world)
					self.ropejoint = SlideJoint(self.shape.body, shape.body, (0, 0), (0, 0), PLAYERSIZE+2, PLAYERSIZE+5)
					world.space.add(self.ropejoint)
					break
		if self.shape.body.position.y > HEIGHT:
			self.dead = True
		return
	# Sets up the collision handlers
	def setupCollisionHandlers(self, world):
		world.addCollisionHandler(self, PLAYERCOLLISIONTYPE, GROUNDCOLLISIONTYPE, 'touchingGround')
		return
	# Collision callbacks for Pymunk, defined here so all instances of Climber can use it without overriding each other.
	# Used for reading in collision points
	# and determining if there is enough ground for the player to jump.
	# Also does a bit of error-checking to see if the player is standing still
	# on a perfectly horizontal surface, which will not activate the collision points.
	def touchingGround(self, space, arbiter, world):
		global JUMPINGDIFFERENCE
		keys = pygame.key.get_pressed()
		bb = self.shape.cache_bb() 
		for shape in arbiter.shapes[0:]:
			for contact in arbiter.contacts:
				if contact.position.y > self.shape.body.position.y:
					if contact.position.x >= bb.left+JUMPINGDIFFERENCE and contact.position.x <= bb.right-JUMPINGDIFFERENCE:
						self.canJump = True
		return True
	def decreaseActionTimer(self):
		if self.actionTimer > 0:
			self.actionTimer -= 1
		return
	def Do(self, world):
		global ROTSPEED, MAXROTSPEED, RIGHTKEY, LEFTKEY, JUMPKEY, ACTIONKEY, JUMPLENGTHEN, ACTIONLENGTH, MAXSPEED, PLAYERFRICTION
		keys = pygame.key.get_pressed()
		vec = self.shape.body.velocity/10
		if self.ropejoint != None:
			if keys[RIGHTKEY]:
				vec.x = PLAYERROPESPEED
				self.shape.body.angular_velocity += ROTSPEED/3
			if keys[LEFTKEY]:
				vec.x = -PLAYERROPESPEED
				self.shape.body.angular_velocity -= ROTSPEED/3
		else:
			if self.canJump:
				if keys[RIGHTKEY]:
					if self.shape.body.velocity.x <= 0:
						vec.x += PLAYERGROUNDSPEED*TURNAROUNDQUICKNESS
					else:
						vec.x += PLAYERGROUNDSPEED
					self.shape.body.angular_velocity += ROTSPEED
				if keys[LEFTKEY]:
					if self.shape.body.velocity.x >= 0:
						vec.x -= PLAYERGROUNDSPEED*TURNAROUNDQUICKNESS
					else:
						vec.x -= PLAYERGROUNDSPEED
					self.shape.body.angular_velocity -= ROTSPEED
			else:
				if keys[RIGHTKEY]:
					vec.x += PLAYERAIRSPEED
					self.shape.body.angular_velocity += ROTSPEED/2
				if keys[LEFTKEY]:
					vec.x -= PLAYERAIRSPEED
					self.shape.body.angular_velocity -= ROTSPEED/2
		# Do other stuff
		if keys[JUMPKEY]:
			#print 'Read the up key'
			#print '*'*20
			if self.canJump == True:
				vec.y = -(PLAYERJUMPHEIGHT+abs(vec.x*HORIZONTALJUMPEFFECT))
				self.canJump = False
				self.canLengthenJump = True
			elif self.canLengthenJump == True:
				if self.shape.body.velocity.y <= JUMPLENGTHEN:
					vec.y = -(PLAYERJUMPHEIGHT/self.jumpLengthen)
					self.jumpLengthen += 1
					if self.jumpLengthen >= JUMPLENGTHEN:
						self.canLengthenJump = False
						self.jumpLengthen = 1
			if self.ropejoint != None:
				self.removeJoints(world)
				vec *= 3
		if keys[DOWNKEY]:
			self.removeJoints(world)
		self.shape.body.apply_impulse(vec)
		self.checkVelocities()
		if keys[ACTIONKEY]:
			if self.actionTimer == 0:
				self.performAction(world)
				self.actionTimer = ACTIONLENGTH
		self.updateCamera(world)
		return
	def updateCamera(self, world):
		if self.shape.body.position.x > CAMERAX:
			if self.screenPosition.x < CAMERAX:
				world.camera.move((self.screenPosition.x-CAMERAX, 0))
		if self.shape.body.position.x < world.camera.backgrounds[0].get_height()-CAMERAX:
			if self.screenPosition.x > WIDTH-CAMERAX:
				world.camera.move((self.screenPosition.x-(WIDTH-CAMERAX), 0))
		if self.shape.body.position.y > CAMERAY:
			if self.screenPosition.y < CAMERAY:
				world.camera.move((0, self.screenPosition.y-CAMERAY))
		if self.shape.body.position.y < world.camera.backgrounds[0].get_height()-CAMERAY:
			if self.screenPosition.y > HEIGHT-CAMERAY:
				world.camera.move((0, self.screenPosition.y-(HEIGHT-CAMERAY)))
		return
	def performAction(self, world):
		self.removeJoints(world)
		return
	def removeJoints(self, world):
		try:
			world.space.remove(self.ropejoint)
			del self.ropejoint
			self.ropejoint = None
			#print 'Removed joint'
		except:
			#print 'Could not remove joint'
			pass
		return
	def checkVelocities(self):
		'''if self.shape.body.velocity.x > MAXSPEED:
			self.shape.body.velocity.x = MAXSPEED
		elif self.shape.body.velocity.x < -MAXSPEED:
			self.shape.body.velocity.x = -MAXSPEED'''
		if self.shape.body.angular_velocity > MAXROTSPEED:
			self.shape.body.angular_velocity = MAXROTSPEED
		elif self.shape.body.angular_velocity < -MAXROTSPEED:
			self.shape.body.angular_velocity = -MAXROTSPEED
		return
	def Draw(self, world):
		#print self.shape.body.angle
		newimg = pygame.transform.rotate(world.getImage('felix'), self.shape.body.angle*-180/3.14)
		newimg.convert()
		newimg.set_alpha(230)
		position = world.camera.findPos(self.shape.body.position)
		self.screenPosition = Vec2d(position)
		world.screen.blit(newimg, (position-Vec2d(newimg.get_width()/2, newimg.get_height()/2)))
		#world.screen.blit(self.image, self.shape.body.position.int_tuple)
		#pygame.draw.circle(world.screen, (0, 255, 0), self.shape.body.position.int_tuple, int(self.shape.radius))
		#pygame.draw.line(world.screen, (255, 0, 0), self.shape.body.position.int_tuple, (self.shape.body.position+self.shape.body.rotation_vector*self.shape.radius).int_tuple, 2)
		#pygame.draw.polygon(world.screen, (0, 255, 0), self.shape.get_points())
		return
