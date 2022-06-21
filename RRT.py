import pygame
import random
import math
import numpy as np

# Constants
WIDTH, HEIGHT = 640, 480
WINDOW = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption('RRT')
FPS = 60

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (189, 154, 122)


NUM_NODES = 5000 #  Max number of nodes/vertices
EPSILON = 10.0 # Step size

def draw_window():
	"""Draw the window all white."""
	WINDOW.fill(WHITE)

def generate_random_node():
	# q_rand(x_rand, y_rand)
	x, y = random.uniform(0, WIDTH), random.uniform(0, HEIGHT)
	# pygame.draw.circle(surface=WINDOW, color=GREEN, center=(x, y), radius=3)

	return x, y

def euclidean_distance(p1, p2):
	"""Euclidean distance between two points.

	Parameters
	----------
	p1 : int
		Start point.
	p2 : int 
		End point.

	Returns
	-------
	float
		Euclidean distance metric.
	"""
	return  math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 

def nearest_neighbor(tree, x_rand):
	"""Returns the index of the nearest neighbor.
	
	The nearest neighbor from all the nodes in the tree
	to the random generated node.

	Parameters
	----------
	tree : list
		Tree containing all the coordinate nodes.
	x_rand : tuple 
		Coordinate of the random node generated.

	Returns
	-------
	tuple
		Nearest node to the random node generated.	
	"""
	distances = []
	for state in tree:
		distance = euclidean_distance(state, x_rand)
		distances.append(distance)

	x_near = tree[np.argmin(distances)]

	return x_near

def new_state(x_rand, x_near):
	"""Advances a small step (EPSILON) towards the random node.
	
	Takes small step (EPSILON) from the nearest node to the
	random node, if the distance is greater than the small step.
	Otherwise, takes the smallest distance computed by the metric
	distance.

	Parameters
	----------
	x_rand : tuple
		Coordinate of the random node generated.
	x_near : tuple 
		Coordinate of the nearest neighbor node.

	Returns
	-------
	tuple
		New node generated between the nearest and random nodes.	
	"""
	if euclidean_distance(x_near, x_rand) < EPSILON:
		# Keep that shortest distance from x_near to x_rand
		return x_rand
	else:
		px, py = x_rand[0] - x_near[0], x_rand[1] - x_near[1]
		theta = math.atan2(py, px)
		x_new = x_near[0] + EPSILON*math.cos(theta), x_near[1] + EPSILON*math.sin(theta)

		return x_new


def main():
	clock = pygame.time.Clock()
	run = True
	x_init = WIDTH//2, HEIGHT//2
	tree = [] # Tree containing all the nodes/vertices
	tree.append(x_init) # Append initial state
	draw_window()
	k = 0
	while run and k < NUM_NODES:
		# Make sure the loop runs at 60 FPS
		clock.tick(FPS)  
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		x_rand = generate_random_node() # Random node 
		x_near = nearest_neighbor(tree, x_rand) # Nearest neighbor to the random node
		x_new = new_state(x_rand, x_near) # New node
		tree.append(x_new)

		pygame.draw.circle(surface=WINDOW, color=BLUE, center=x_init, radius=3)
		pygame.draw.circle(surface=WINDOW, color=BROWN, center=x_new, radius=3)
		pygame.draw.line(surface=WINDOW, color=BLACK, start_pos=x_near, end_pos=x_new)
		pygame.display.update()
		
		k += 1

	pygame.quit()

if __name__ == '__main__':
	main()