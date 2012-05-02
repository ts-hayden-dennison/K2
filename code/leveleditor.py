#! usr/bin/env python

import pygame
from sys import exit, argv
from K2 import *
import math
import pymunk
from vector import Vector
from createshapes import *
from pgu import gui
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
background = imgload(argv[2])
leveldata = []
objects = {}
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

def setProperties(classname):
	return []

# Functions for creating all the different shapes
# Create polygons, convex or concave (the concave polygon is triangulated)
def definePoly():
	global CLIPPINGRADIUS, clock, world, leveldata
	pos = pygame.mouse.get_pos()
	center = pos[:]
	points = [pos[:]]
	polypoints = [(0, 0)]
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
					if findDistance(e.pos, point) < CLIPPINGRADIUS:
						if pymunk.util.is_convex(points):
							poly = Poly(world, center, polypoints)
							world.addObject(poly)
							index = len(leveldata)
							leveldata.append(('Poly', center, polypoints))
							objects[poly] = index
							return
						else:
							triangles = pymunk.util.triangulate(polypoints)
							for pointslist in triangles:
								poly = Poly(world, center, pointslist)
								world.addObject(poly)
								index = len(leveldata)
								leveldata.append(('Poly', center, pointslist))
								objects[poly] = index
							return
			polypoint = (Vector(e.pos[0], e.pos[1])-Vector(center[0], center[1])).int_tuple()
			polypoints.append(polypoint)
			points.append(e.pos)
		screen.blit(background, (0, 0))
		world.draw()
		for point in points:
			pygame.draw.circle(screen, (255, 255, 0), point, CLIPPINGRADIUS)
			if points.index(point) > 0:
				pygame.draw.line(screen, (255, 255, 255), point, points[points.index(point)-1], 3)
		if len(points) > 0:
			pygame.draw.line(screen, (255, 255, 255), points[-1], pygame.mouse.get_pos(), 3)
		pygame.draw.circle(screen, (255, 0, 0), center, 3)
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
	return
def editPoly(data):
	print data
	return
def editClimber(climber, index):
	last = climber.shape.body.position
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
		elif e.type == pygame.MOUSEBUTTONUP:
			leveldata[index][1] = last.int_tuple
			world.update()
			return
		elif e.type == pygame.MOUSEMOTION:
			last += e.pos-last
		climber.shape.body.position = last
		screen.blit(background,(0, 0))
		world.draw()
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
	return
# Create circles
def defineCircle():
	global leveldata, world
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
			world.addObject(circle)
			index = len(leveldata)
			leveldata.append(('Circle',  center.int_tuple(), radius))
			objects[circle] = index
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
	global leveldata, world
	pos = pygame.mouse.get_pos()
	world.addObject(Goal(world, pos))
	leveldata.append(['Goal', pos])
# Drop climbers
def defineClimber():
	global leveldata, world
	pos = pygame.mouse.get_pos()
	climber = Climber(world, pos)
	world.addObject(climber)
	index = len(leveldata)
	leveldata.append(['Climber', pos])
	objects[climber] = index
# Convienience function for creating springs
def defineSpring():
	global leveldata, world
	pos = pygame.mouse.get_pos()
	spring = Spring(world, pos)
	world.addObject(spring)
	index = len(leveldata)
	leveldata.append(['Spring', pos])
	objects[spring] = index
	return
# Convienience function for creating perfect rectangles
def defineBlock():
	global leveldata, world
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
			world.addObject(block)
			index = len(leveldata)
			leveldata.append(['Block', (startpos[0]+width/2, startpos[1]+height/2), (width, height)])
			objects[block] = index
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
# Convienience function for creating death areas
def defineDeathBox():
	global leveldata, world
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
		elif e.type == pygame.MOUSEBUTTONUP:
			world.addObject(DeathBox(world, (startpos[0]+width/2, startpos[1]+height/2), (width, height)))
			leveldata.append(('DeathBox', (startpos[0]+width/2, startpos[1]+height/2), (width, height)))
			return
		endpos = pygame.mouse.get_pos()
		screen.blit(background, (0, 0))
		world.draw()
		width, height = (endpos[0]-startpos[0], endpos[1]-startpos[1])
		pygame.draw.rect(screen, (255, 0, 0), (startpos, (width, height)))
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
	return
# Function for putting text into the world
def defineText():
	pos = pygame.mouse.get_pos()
	text = raw_input('Enter text: ')
	world.addObject(Text(world, pos, "'"+text+"'"))
	leveldata.append(('Text', pos, "'"+text+"'"))
	return
# Draws the cursor lines
def drawHelpers():
	pos = pygame.mouse.get_pos()
	pygame.draw.line(screen, (255, 0, 0), (pos[0], 0), (pos[0], HEIGHT), 1)
	pygame.draw.line(screen, (255, 0, 0), (0, pos[1]), (screen.get_width(), pos[1]), 1)
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
			world.addObject(rope)
			index = len(leveldata)
			leveldata.append(('Rope', position, length))
			objects[rope] = index
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
	shapes = world.space.point_query(position)
	index = -1
	editObject = None
	for shape in shapes:
		for ob in world.getObjects():
			try:
				if ob.shape == shape:
					index = objects[ob]
					editObject = ob
					break
			except:
				if shape in ob.shapes:
					index = objects[ob]
					editObject = ob
					break
	if index != -1:
		item = leveldata[index]
		exec('edit'+item[0]+'(editObject, index)')
		return
	return
def main():
	global leveldata
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
	items.extend([Item(polyimage, 'Poly'), Item(climberimage, 'Climber'), Item(goalimage, 'Goal'),
		Item(springimage, 'Spring'), Item(deathboximage, 'DeathBox'), Item(blockimage, 'Block'),
		Item(circleimage, 'Circle'), Item(textimage, 'Text'), Item(ropeimage, 'Rope')])
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
				elif e.key == pygame.K_s:
					try:
						name = raw_input('Name of level? ')
						name = os.path.join(LEVELFOLDER, name)
						print name
						filename = open(name, 'w')
						pickle.dump(leveldata, filename)
						filename.close()
					except:
						pass
				elif e.key == pygame.K_c:
					world.clear()
					leveldata = []
					objects = {}
				elif e.key == pygame.K_SPACE:
					world.clear()
					loadLevel(world, leveldata)
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
						world.update()
						clock.tick(FPS)
						pygame.display.update()
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
			loadLevel(world, leveldata)
		menu.update()
		drawHelpers()
		clock.tick(FPS)
		pygame.display.update()
if __name__ == '__main__':
	main()
