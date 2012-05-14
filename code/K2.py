#! usr/bin/env python
# A game
# IMPORTS
import pygame
from sys import exit, argv
import pymunk
import random
import os
import pickle
from objects import *
from constants import *
from climber import *
from util import *
from camera import *

###############################################################################
# INITIALIZATION
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption('K2')
clock = pygame.time.Clock()
levels = loadLevels()
currentlevel = 0
if '-nosounds' in argv:
	sound = False
else:
	sound = True
###############################################################################
# LOCAL CLASS DEFINITIONS
class Particle(pygame.sprite.Sprite):
	# A Particle is for special fx. Give its constructor a position and size.
	# Optional arguments include: velocity, color, lifespan
	def __init__(self, position, size, vel=False, color=False, timer=50):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position, (size, size))
		if vel != False:
			self.velocity = vel
		else:
			self.velocity = (random.randint(-10, 10), random.randint(-10, 10))
		if color != False:
			self.color = color
		else:
			self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
		self.timer = timer
	def update(self, particles):
		global screen
		self.timer -= 1
		self.rect = self.rect.move(self.velocity)
		pygame.draw.rect(screen, self.color, self.rect)
		if self.timer <= 0:
			particles.remove(self)
		return
###############################################################################
# WORLD CLASS DEFINITION
class World():
	# The World class is responsible for updating the objects and characters, updating the physics engine,
	# and providing local copies of the global variables in this file.
	# The __init__ method reads in the constants from constants.py and creates the physics engine from the constants
	# It also provides some helper variables: a framerate counter and unique identifiers for every object and character
	# It defines a single event handler in Pymunk: when the player touches the goal, the levelWon() method is called
	# and its complete variable set to True.
	def __init__(self):
		global GRAVITY, DAMPING, ACCURACY, ITERATIONS, PLAYERCOLLISIONTYPE, GOALCOLLISIONTYPE, DEATHCOLLISIONTYPE, sound
		self.clear()
		if sound:
			self.sounds = loadSounds()
		self.images = loadImages()
		self.screen = screen
	# Just calls other methods and updates the timer.
	def update(self):
		self.space.step(self.accuracy)
		self.updateObjects()
		self.checkCompletion()
		self.timer += 1
		return
	# Simply draws all objects at their current position without updating them.
	def draw(self):
		for thing in self.objects:
			thing.Draw(self)
		return
	# A way to have multiple objects with the same collision handlers.
	def addCollisionHandler(self, thing, typea, typeb, funcname, *args):
		name = str(typea)+str(typeb)
		if name not in self.callbacks.keys():
			try:
				self.space.add_collision_handler(typea, typeb, None, self.callbackFunction, None, None, name, funcname)
				self.callbacks[name] = [thing]
			except:
				pass
		else:
			self.callbacks[name].append(thing)
		return
	# The default callback function that is called when an event happens. It makes sure all the objects which requested the callback
	# are notified, ie, their function is called with the right arguments.
	def callbackFunction(self, space, arbiter, name, funcname):
		try:
			for thing in self.callbacks[name]:
				if thing.shape in arbiter.shapes:
					callback = 'thing.'+funcname+'(space, arbiter, self)'
					exec(callback)
					return True
		except:
			pass
		return True
	# A simple way for other objects to play sound effects. Put a sound in the sounds subfolder and it will be exposed
	def playSound(self, name):
		try:
			self.sounds[name].play()
		except:
			pass
		return
	def getImage(self, name):
		try:
			return self.images[name]
		except:
			pass
		return
	# Collision callback for Pymunk
	def PlayerTouchedDeath(self, space, arbiter):
		global levels, currentlevel
		levelFailed(self, "Unfortunately, you are now classified as 'dead'. :D")
		self.clear()
		loadLevel(self, levels[currentlevel])
		return True
	# Kind of a redundant method but it exists so that the user can see he touched the goal onscreen
	def checkCompletion(self):
		if self.complete == True:
			levelComplete(self, 'Level Complete!')
		return
	# Event handler for touching the goal
	def PlayerTouchedGoal(self, space, arbiter):
		self.complete = True
		return True
	# Returns a list of the added objects
	def getObjects(self):
		return self.objects
	# Returns the framerate counter
	def getTime(self):
		return self.timer
	# Adds an object that is a subclass of Object, or a list of Objects
	# Also gives them unique identifiers
	def addObject(self, objects):
		try:
			self.objects.extend(objects)
		except:
			self.objects.append(objects)
		return
	# Removes an object that is a subclass of Object, or a list of Objects
	def removeObject(self, objects):
		try:
			for ob in objects:
				self.objects.remove(ob)
		except:
			if objects != None:
				self.objects.remove(objects)
			else:
				self.objects = []
		return
	# Loops through all added Objects and updates them.
	def updateObjects(self):
		for thing in self.objects:
			thing.update(self)
		return
	# Returns a unique identifier
	def nextId(self):
		old = self.nextIdentification
		self.nextIdentification += 1
		return old
	# Resets everything in the world
	def clear(self):
		self.space = pymunk.Space(ITERATIONS)
		self.space.gravity = GRAVITY
		self.space.damping = DAMPING
		self.accuracy = ACCURACY
		self.space.collision_bias = BIAS
		self.space.add_collision_handler(PLAYERCOLLISIONTYPE, GOALCOLLISIONTYPE, pre_solve=self.PlayerTouchedGoal)
		self.space.add_collision_handler(PLAYERCOLLISIONTYPE, DEATHCOLLISIONTYPE, pre_solve=self.PlayerTouchedDeath)
		self.objects = []
		self.timer = 0
		self.complete = False
		self.nextIdentification = 0
		self.callbacks = {}
		self.camera = Camera()
		return
	def _get_backgrounds(self):
		global backgrounds
		return backgrounds

###############################################################################
# LOCAL FUNCTION DEFINITIONS
def levelComplete(world, caption):
	# Displays a neat level completion animation
	global screen, FPS
	size = 64
	font = pygame.font.Font(None, size)
	text = caption
	y = screen.get_height()/2
	x = screen.get_width()/2-len(text)/2*size/2
	font.set_bold(True)
	background = pygame.Surface((screen.get_width(), screen.get_height()))
	background.set_alpha(25)
	background.fill((50, 50, 100))
	numparticles = 100
	particles = []
	world.playSound('win')
	for i in range(0, numparticles):
		particles.append(Particle((screen.get_width()/2, screen.get_height()/2), random.randint(5, 10), timer=200))
	while True:
		for i in particles:
			i.update(particles)
		screen.blit(background, (0, 0))
		screen.blit(font.render(text, True, (255, random.randint(50, 255), random.randint(50, 200))), (x, y))
		pygame.display.update()
		clock.tick(FPS-10)
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			pygame.quit()
			exit()
		elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
			return
	return

def levelFailed(world, caption):
	# Displays a sad level failed animation
	global screen, FPS
	size = 40
	font = pygame.font.Font(None, size)
	y = screen.get_height()/2
	x = screen.get_width()/2-len(caption)/2*size/2
	font.set_bold(True)
	background = pygame.Surface((screen.get_width(), screen.get_height()))
	background.set_alpha(25)
	background.fill((100, 0, 0))
	timer = 0
	while True:
		world.draw()
		screen.blit(background, (0, 0))
		screen.blit(font.render(caption, True, (255, random.randint(100, 200), 0)), (x, y))
		pygame.display.update()
		clock.tick(FPS-10)
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			pygame.quit()
			exit()
		elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
			return
		timer += 1
	return
###############################################################################
# ENTRY POINT
def main():
	# Runs the game :D
	global FPS, clock, screen, levels, currentlevel
	world = World()
	while True:
		try:
			world.clear()
			loadLevel(world, levels[currentlevel])
		except:
			if currentlevel >= len(levels):
				return
		world.draw()
		pygame.display.update()
		#################################################
		while world.complete == False:
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					pygame.quit()
					exit()
				elif e.type == pygame.KEYDOWN:
					if e.key == pygame.K_ESCAPE:
						pygame.quit()
						exit()
					elif e.key == pygame.K_r:
						try:
							world.clear()
							loadLevel(world, levels[currentlevel])
						except:
							return
			###################################
			screen.blit(world.camera.backgrounds[0], world.camera.findPos((0, 0)))
			world.update()
			for background in world.camera.backgrounds[1:]:
				screen.blit(background, world.camera.findPos((0, 0)))
			clock.tick(FPS)
			pygame.display.flip()
		currentlevel += 1
		####################################
	return
###############################################################################
# boilerplate thingamajigs :)
if __name__ == '__main__':
	main()
