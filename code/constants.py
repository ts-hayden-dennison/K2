#! usr/bin/env python
# Constant values setting
import pygame

# The frames per second the game will *try* to run at
FPS = 100
# Width of application window
WIDTH = 1024
# Height of application window
HEIGHT = 640
# Force of gravity in the physics simulation
GRAVITY = (0, 3000.0)
# Basically air humidity
DAMPING = 0.40
# Divide by a larger value for more accuracy in the physics engine
# divide by a smaller value for more speed
ACCURACY = 1/200.0
# How many times the elasticity solver should resolve conflicts in a single frame
ITERATIONS = 10
# How far objects can penetrate
BIAS = 0.0
# Width and height of player box
PLAYERSIZE = 14
# Walking speed of the player
PLAYERSPEED = 1000
# Initial jump velocity
PLAYERJUMPHEIGHT = 10000
# How heavy the player is
PLAYERMASS = 90
# Rubber or ice! :)
PLAYERFRICTION = 1.0
# How bouncy the player is
PLAYERBOUNCE = 0.5
# The maximum walking velocity of the player
#MAXSPEED = 3000
# The key set for right movement
RIGHTKEY = pygame.K_RIGHT
# The key set for left movement
LEFTKEY = pygame.K_LEFT
# The key used for jumping
JUMPKEY = pygame.K_UP
# The key used for something
ACTIONKEY = pygame.K_z
# The key set for skidding
DOWNKEY = pygame.K_DOWN
# The maximum amount of vertical velocity; think of Mario: hold down for higher jumps
JUMPLENGTHEN = 25
# How many frames between each action button event
ACTIONLENGTH = 0
# The rotation speed of the player
ROTSPEED = 2
# How fast the player can rotate
MAXROTSPEED = 360
# The difference from the sides of the player's body at which
# the player cannot jump off a side of a polygon.
JUMPINGDIFFERENCE = 0
# How much the player's running speed affects his jumping height
HORIZONTALJUMPEFFECT = 10
# Collision types. Don't set one to zero, or the physics engine will crash, and therefore, the game.
GROUNDCOLLISIONTYPE = 2
GOALCOLLISIONTYPE = 3
PLAYERCOLLISIONTYPE = 1
DEATHCOLLISIONTYPE = 4
ROPECOLLISIONTYPE = 5
# Directory locations
IMAGEFOLDER = 'images'
SOUNDFOLDER = 'sounds'
CODEFOLDER = 'code'
LEVELFOLDER = 'levels'
# The color of the background
BACKGROUNDCOLOR = (0, 0, 0)
# how awesome the background is
BACKGROUNDAWESOMENESS = 200
# Sizes of rope segments
ROPESIZE = 5
# This determines how "stiff" the rope feels
ROPESTIFFNESS = 3
