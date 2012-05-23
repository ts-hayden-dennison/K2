#! usr/bin/env python

import pygame
from sys import exit, argv
from K2 import *
import math
import pymunk
from pymunk import Vec2d
from vector import Vector
from createshapes import *
import os
from constants import *
import pickle
from objects import *
from climber import *
import random

pygame.init()
screen = pygame.display.set_mode((WIDTH+28, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space
world = World()
CLIPPINGRADIUS = 5
try:
	background = imgload(argv[2])
except:
	background = pygame.Surface((640, 480))
lastCameraPos = Vec2d()
class Menu():
	def __init__(self, position, items=[]):
		self.items = items
		self.itemrects = []
		self.pos = position
		self.spacing = 32
		self.selected = 0
		for item in self.items:
			rect = item.image.get_rect()
			rect.topleft = (self.pos+Vector(0, (self.spacing*self.items.index(item)+1))).int_tuple()
			self.itemrects.append(rect)
	def update(self):
		global screen
		for item in self.items:
			screen.blit(item.image, self.itemrects[self.items.index(item)])
		pos = pygame.mouse.get_pos()
		buttons = pygame.mouse.get_pressed()
		for rect in self.itemrects:
			if rect.collidepoint(pos):
				if buttons[0] == 1:
					self.selected = self.itemrects.index(rect)
		if len(self.itemrects) > 0:
			pygame.draw.rect(screen, (255, 0, 0), self.itemrects[self.selected], 2)
		return
	def returnSelected(self):
		return self.items[self.selected].name

class Item():
	def __init__(self, image, name):
		self.image = image
		self.name = name

def findDistance(p1, p2):
	x, y = p1
	x2, y2 = p2
	distance = math.sqrt((x2-x)**2+(y2-y)**2)
	return distance

# Functions for creating all the different shapes
# Create polygons, convex or concave (the concave polygon is triangulated)
def defineGroundPoly():
	global CLIPPINGRADIUS, clock, world
	center = lastCameraPos+Vec2d(pygame.mouse.get_pos())
	points = [Vec2d(center.x, center.y)]
	polypoints = [Vec2d(0, 0)]
	while True:
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			elif e.key == pygame.K_BACKSPACE:
				return
		elif e.type == pygame.MOUSEBUTTONDOWN:
			if len(points) >= 3:
				for point in points:
					if findDistance(lastCameraPos+e.pos, point) < CLIPPINGRADIUS:
						if pymunk.util.is_convex(points):
							for vert in polypoints:
									polypoints[polypoints.index(vert)] = vert.int_tuple
							poly = GroundPoly(world, center.int_tuple, polypoints)
							return
						else:
							triangles = pymunk.util.triangulate(polypoints)
							polys = pymunk.util.convexise(triangles)
							for pointslist in polys:
								for vert in pointslist:
									pointslist[pointslist.index(vert)] = vert.int_tuple
								poly = GroundPoly(world, center.int_tuple, pointslist)
							return
			polypoints.append((Vec2d(e.pos)-(center))+lastCameraPos)
			points.append(lastCameraPos+Vec2d(e.pos))
		screen.blit(background, (0, 0))
		world.draw()
		for point in points:
			pygame.draw.circle(screen, (255, 255, 0), world.camera.findPos(point).int_tuple, CLIPPINGRADIUS)
			if points.index(point) > 0:
				pygame.draw.line(screen, (255, 255, 255), world.camera.findPos(point).int_tuple, world.camera.findPos(points[points.index(point)-1]).int_tuple, 3)
		if len(points) > 0:
			pygame.draw.line(screen, (255, 255, 255), world.camera.findPos(points[-1]).int_tuple, pygame.mouse.get_pos(), 3)
		pygame.draw.circle(screen, (255, 0, 0), world.camera.findPos(center).int_tuple, 3)
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
	return

# Create circles
def defineCircle():
	center = Vector.from_tuple(pygame.mouse.get_pos())
	radius = 0
	while True:
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			pygame.quit
			exit()
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			elif e.key == pygame.K_BACKSPACE:
				return
		elif e.type == pygame.MOUSEBUTTONDOWN:
			circle = Circle(world, center.int_tuple(), radius)
			return
		pos = pygame.mouse.get_pos()
		radius = (center-Vector.from_tuple(pos)).get_mag()
		screen.blit(background, (0, 0))
		world.draw()
		pygame.draw.circle(screen, (255, 255, 255), center.int_tuple(), int(radius))
		clock.tick(FPS)
		pygame.display.update()
	return
# Convienience function for creating goals
def defineGoal():
	pos = pygame.mouse.get_pos()
	Goal(world, pos)
# Drop climbers
def defineClimber():
	pos = lastCameraPos+pygame.mouse.get_pos()
	climber = Climber(world, pos.int_tuple)
	return
# Convienience function for creating springs
def defineSpring():
	pos = pygame.mouse.get_pos()
	spring = Spring(world, pos)
	return
# Convienience function for creating perfect rectangles
def defineBlock():
	startpos = pygame.mouse.get_pos()
	endpos = pygame.mouse.get_pos()
	width, height = (endpos[0]-startpos[0], endpos[1]-startpos[1])
	while True:
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			elif e.key == pygame.K_BACKSPACE:
				return
		elif e.type == pygame.MOUSEBUTTONDOWN:
			block = Block(world, (startpos[0]+width/2, startpos[1]+height/2), (width, height))
			return
		endpos = pygame.mouse.get_pos()
		screen.blit(background, (0, 0))
		world.draw()
		width, height = (endpos[0]-startpos[0], endpos[1]-startpos[1])
		pygame.draw.rect(screen, (255, 255, 255), (startpos, (width, height)))
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
	return
def defineNPC():
	pos = lastCameraPos+pygame.mouse.get_pos()
	enemy = NPC(world, pos.int_tuple)
# Function for putting text into the world
def defineText():
	pos = pygame.mouse.get_pos()
	text = raw_input('Enter text: ')
	Text(world, pos, "'"+text+"'")
	return
# Draws the cursor lines
def drawHelpers():
	global lastCameraPos
	pos = pygame.mouse.get_pos()
	pygame.draw.line(screen, (255, 0, 0), (pos[0], 0), (pos[0], HEIGHT), 1)
	pygame.draw.line(screen, (255, 0, 0), (0, pos[1]), (screen.get_width(), pos[1]), 1)
	keys = pygame.key.get_pressed()
	vec = Vec2d()
	if keys[pygame.K_w]:
		vec.y = -10
	if keys[pygame.K_s]:
		vec.y = 10
	if keys[pygame.K_d]:
		vec.x = 10
	if keys[pygame.K_a]:
		vec.x = -10
	world.camera.move(vec)
	lastCameraPos += vec
	return

# Function for defining ropes
def defineRope():
	position = pygame.mouse.get_pos()
	while True:
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			pygame.quit()
			exit()
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				pygame.quit()
				exit()
			elif e.key == pygame.K_BACKSPACE:
				return
		elif e.type == pygame.MOUSEBUTTONDOWN:
			length = abs(e.pos[1]-position[1])
			rope = Rope(world, position, length)
			return
		endpos = list(pygame.mouse.get_pos())
		screen.blit(background, (0, 0))
		world.draw()
		pygame.draw.line(screen, (255, 170, 50), position, endpos, 2)
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
	return

def setProperties(position):
	shapes = world.space.point_query(lastCameraPos+position)
	for shape in shapes:
		for ob in world.getObjects():
			try:
				if ob.shape == shape:
					world.removeObject(ob)
					del ob
					break
			except:
				if shape in ob.shapes:
					world.removeObject(ob)
					del ob
					break
	return

def getData():
	# Loads a list version of the data in the World class so it can be rebuilt.
	pickledata = []
	objects = world.getObjects()
	for ob in objects:
		if isinstance(ob, Climber):
			pickledata.append(('Climber', ob.shape.body.position.int_tuple))
		if isinstance(ob, GroundPoly):
			pickledata.append(('GroundPoly', ob.shape.body.position.int_tuple, ob.shape.get_points(), ob.shape.body.is_static))
		if isinstance(ob, DeathPoly):
			pickledata.append(('DeathPoly', ob.shape.body.position.int_tuple, ob.shape.get_points(), ob.shape.body.is_static))
		if isinstance(ob, ClingPoly):
			pickledata.append(('ClingPoly', ob.shape.body.position.int_tuple, ob.shape.get_points(), ob.shape.body.is_static))
		if isinstance(ob, AlivePoly):
			pickledata.append(('AlivePoly', ob.shape.body.position.int_tuple, ob.shape.get_points(), ob.shape.body.is_static))
		if isinstance(ob, NPC):
			pickledata.append(('NPC', ob.shape.body.position.int_tuple))
		if isinstance(ob, GroundCircle):
			pickledata.append(('GroundCircle', ob.shape.body.position.int_tuple, int(ob.shape.radius), ob.shape.body.is_static))
		if isinstance(ob, DeathCircle):
			pickledata.append(('DeathCircle', ob.shape.body.position.int_tuple, int(ob.shape.radius), ob.shape.body.is_static))
		if isinstance(ob, ClingCircle):
			pickledata.append(('ClingCircle', ob.shape.body.position.int_tuple, int(ob.shape.radius), ob.shape.body.is_static))
		if isinstance(ob, AliveCircle):
			pickledata.append(('AliveCircle', ob.shape.body.position.int_tuple, int(ob.shape.radius), ob.shape.body.is_static))
		if isinstance(ob, Rope):
			pickledata.append(('Rope', ob.shapes[0].body.position.int_tuple, ob.length))
	return pickledata
def main():
	# Create all the menu images and things
	items = []
	polyimage = pygame.Surface((28, 28))
	polyimage.fill((0, 0, 0))
	pygame.draw.polygon(polyimage, (255, 255, 255), ((13, 0), (0, 28), (28, 28)), 3)
	climberimage = pygame.Surface((28, 28))
	climberimage.fill((0, 0, 0))
	pygame.draw.circle(climberimage, (0, 255, 0), (14, 14), 13)
	goalimage = pygame.Surface((28, 28))
	pygame.draw.rect(goalimage, (255, 255, 0), (0, 7, 28, 7))
	springimage = pygame.Surface((28, 28))
	pygame.draw.rect(springimage, (0, 255, 255), (0, 7, 28, 7))
	deathboximage = pygame.Surface((24, 24))
	deathboximage.fill((255, 0, 0))
	blockimage = pygame.Surface((28, 28))
	blockimage.fill((255, 255, 255))
	circleimage = pygame.Surface((28, 28))
	circleimage.fill((0, 0, 0))
	pygame.draw.circle(circleimage, (255, 255, 255), (14, 14), 13)
	textimage = pygame.Surface((28, 28))
	textimage.fill((0, 0, 0))
	font = pygame.font.Font(None, 25)
	textimage.blit(font.render('A', True, (255, 255, 255)), (2, 2))
	ropeimage = pygame.Surface((28, 28))
	ropeimage.fill((0, 0, 0))
	pygame.draw.line(ropeimage, (255, 170, 50), (14, 0), (14, 28), 1)
	enemyimage = pygame.Surface((28, 28))
	pygame.draw.circle(enemyimage, (200, 200, 200), (14, 14), 14)
	items.extend([Item(polyimage, 'GroundPoly'), Item(climberimage, 'Climber'), Item(goalimage, 'Goal'),
		Item(springimage, 'Spring'), Item(deathboximage, 'DeathBox'), Item(blockimage, 'Block'),
		Item(circleimage, 'Circle'), Item(textimage, 'Text'), Item(ropeimage, 'Rope'), Item(enemyimage, 'NPC')])
	menu = Menu(Vector(WIDTH, 0), items)
	# Run the level editor
	while True:
		screen.blit(background, (0, 0))
		pygame.draw.line(screen, (255, 255, 255), (WIDTH-1, 0), (WIDTH-1, HEIGHT), 1)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				exit()
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					pygame.quit()
					exit()
				elif e.key == pygame.K_RETURN:
					try:
						name = raw_input('Name of level? ')
						name = os.path.join(LEVELFOLDER, name)
						print name
						filename = open(name, 'w')
						pickle.dump(getData(), filename)
						filename.close()
					except:
						pass
				elif e.key == pygame.K_c:
					world.clear()
				elif e.key == pygame.K_SPACE:
					newworld = World()
					loadLevel(newworld, getData())
					while world.complete == False:
						e = pygame.event.poll()
						if e.type == pygame.QUIT:
							pygame.quit()
							exit()
						elif e.type == pygame.KEYDOWN:
							if e.key == pygame.K_ESCAPE:
								pygame.quit()
								exit()
							elif e.key == pygame.K_BACKSPACE:
								break
						screen.blit(background, (0, 0))
						newworld.update()
						clock.tick(FPS)
						pygame.display.update()
					del newworld
			elif e.type == pygame.MOUSEBUTTONDOWN:
				if e.pos[0] < WIDTH:
					if e.button == 1:
						name = menu.returnSelected()
						exec('define'+name+'()')
					else:
						setProperties(e.pos)
		world.draw()
		if world.complete == True:
			world.clear()
			loadLevel(world, getData())
		menu.update()
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
if __name__ == '__main__':
	main()
