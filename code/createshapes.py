#! usr/bin/env python
# These are all utilities to create shapes for Pymunk
import pymunk as pm
# Function definitions

# This function creates a Pymunk poly in the shape of a box.
# Pass it a position and size
# Optional arguments: mass, friction, elasticity, static
def createBox(position, size, mass=20, friction=20, elasticity=0.5, static=False):
	position = pm.Vec2d(position)
	size = pm.Vec2d(size)
	vertices = ((0, 0), (0, size.y), (size.x, size.y), (size.x, 0))
	if static == False:
		inertia = pm.moment_for_poly(mass, vertices)
		body = pm.Body(mass, inertia)
	else:
		body = pm.Body(None, None)
	body.position = position
	box = pm.Poly.create_box(body, size)
	box.friction = friction
	box.elasticity = elasticity
	return box

# This function creates a Pymunk poly with a set of vertices
# Pass it vertices and position
# Optional arguments: mass, friction, elasticity, static
def createPolygon(position, vertices, mass=20, friction=20, elasticity=0.5, static=False):
	position = pm.Vec2d(position)
	if static == False:
		inertia = pm.moment_for_poly(mass, vertices)
		body = pm.Body(mass, inertia)
	else:
		body = pm.Body(None, None)
	body.position = position
	poly = pm.Poly(body, vertices)
	poly.friction = friction
	poly.elasticity = elasticity
	return poly

# Creates a Pymunk circle
# Pass it a position and radius
# Optional arguments: mass, friction, elasticity, static
def createBall(position, radius, mass=20, friction=20, elasticity=0.5, static=False):
	position = pm.Vec2d(position)
	if static == False:
		inertia = pm.moment_for_circle(mass, 0, radius)
		body = pm.Body(mass, inertia)
	else:
		body = pm.Body(None, None)
	body.position = position
	ball = pm.Circle(body, radius)
	ball.friction = friction
	ball.elasticity = elasticity
	return ball
