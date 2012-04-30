#! usr/bin/env python
# Utilities for loading levels
import os
from constants import *
import pickle
import pygame
from objects import *
from climber import *
import random

def loadLevels():
	levels = []
	for levelfile in os.listdir(os.path.join('.', LEVELFOLDER)):
		leveldata = open(os.path.join(LEVELFOLDER, levelfile), 'rb')
		try:
			levels.append(pickle.load(leveldata))
		except:
			print 'There was a problem loading the level ' + levelfile + '.'
			print 'The file may be corrupted.'
		leveldata.close()
	return levels

def randomColor():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
def randomPos():
	return (random.randint(0, WIDTH), random.randint(0, HEIGHT))
def randomRect():
	return pygame.Rect(randomPos(), randomPos(), randomPos(), randomPos())

def loadLevel(world, data):
	# Loop through commands and run the needed methods
	for command in data:
		string = command[0]+"(world"
		for i in command[1:]:
			string = string+", "+i.__str__()
		string = string+")"
		exec(string) 
	return

def loadSounds():
	# Loads all sounds in the 'sounds' subfolder
	sounds = {}
	for sound in os.listdir(os.path.join('.', SOUNDFOLDER)):
		sounds[sound[0:-4]] = pygame.mixer.Sound(os.path.join(SOUNDFOLDER, sound))
	return sounds

def imgload(filename, colorkey=(255, 255, 255)):
	path = os.path.join('.', IMAGEFOLDER)
	path = os.path.join(path, filename)
	try:
		image = pygame.image.load(path)
	except:
		raise SystemError, "Could not load " + path
	image.set_colorkey(colorkey)
	return image
