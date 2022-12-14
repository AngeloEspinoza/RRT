import pygame
import environment
import graph 
import argparse
import sys

# Command line arguments
parser = argparse.ArgumentParser(description='Implements the RRT algorithm for path planning.')
parser.add_argument('-o', '--obstacles', type=bool, action=argparse.BooleanOptionalAction,
	metavar='', required=False, help='Obstacles on the map')
parser.add_argument('-n', '--nodes', type=int, metavar='', required=False,
	help='Maximum number of nodes')
parser.add_argument('-e', '--epsilon', type=float, metavar='', required=False, help='Step size')
parser.add_argument('-init', '--x_init', nargs='+', type=int, metavar='', required=False,
	help='Initial node position in X and Y, respectively')
parser.add_argument('-goal', '--x_goal', nargs='+', type=int, metavar='', required=False,
	help='Goal node position in X and Y, respectively')
parser.add_argument('-srn', '--show_random_nodes', type=bool, action=argparse.BooleanOptionalAction,
	metavar='', required=False, help='Show random nodes on screen')
parser.add_argument('-snn', '--show_new_nodes', type=bool, action=argparse.BooleanOptionalAction,
	metavar='', required=False, help='Show new nodes on screen')
parser.add_argument('-bp', '--bias_percentage', type=int, metavar='', required=False, default=30,
	help='Amount of bias the RRT from 1 to 100')
parser.add_argument('-ptg', '--path_to_goal', type=bool, action=argparse.BooleanOptionalAction, 
	metavar='', required=False, help='Draws a red line indicating the path to goal')
parser.add_argument('-mr', '--move_robot', type=bool, action=argparse.BooleanOptionalAction, 
	metavar='', required=False, help='Shows the movements of the robot from the start to the end')
parser.add_argument('-kt', '--keep_tree', type=bool, action=argparse.BooleanOptionalAction, 
	metavar='', required=False, help='Keeps the tree while the robot is moving towards the goal')
args = parser.parse_args()

# Initialization 
pygame.init()

# Constants
MAP_DIMENSIONS = 640, 480

# RRT parameters
MAX_NODES = args.nodes if args.nodes is not None else 5000 # Maximum number of nodes/vertices
EPSILON = args.epsilon if args.epsilon is not None else 7.0 # Step size

# Initial and final position of the robot
x_init = tuple(args.x_init) if args.x_init is not None else (50, 50) # Initial node
x_goal = tuple(args.x_goal) if args.x_goal is not None else (540, 380) # Goal node

# Instantiating the environment and the graph
environment_ = environment.Environment(map_dimensions=MAP_DIMENSIONS)
graph_ = graph.Graph(start=x_init, goal=x_goal, map_dimensions=MAP_DIMENSIONS, epsilon=EPSILON)

def main():
	clock = pygame.time.Clock()
	run = True
	is_goal_reached = False
	is_simulation_finished = False
	tree = [] # Tree list containing all the nodes/vertices
	parent = [] # Parent list of each each node/vertex
	values = [] # Values list of each node/vertex
	tree.append(x_init) # Append initial node
	parent.append(0) # Append initial parent
	obstacles = environment_.draw_obstacles() if args.obstacles else []

	k = 0
	node_value = 0
	iteration = 0
	bias_percentage = 10 - args.bias_percentage//10 if args.bias_percentage != 100 else 1
	
	nears = [] # To store the generated x_near nodes 

	while run and k < MAX_NODES:
		# Make sure the loop runs at 60 FPS
		clock.tick(environment_.FPS)  
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# Draw points and lines for visualization
		graph_.draw_initial_node(map_=environment_.map)
		graph_.draw_goal_node(map_=environment_.map)

		if not is_simulation_finished:
			# Sample free space and check x_rand node collision
			x_rand = graph_.generate_random_node() # Random node 
			rand_collision_free = graph_.is_free(point=x_rand, obstacles=obstacles) 
		
			if rand_collision_free:
				x_near = graph_.nearest_neighbor(tree, x_rand) # Nearest neighbor to the random node
				x_new = graph_.new_state(x_rand, x_near, x_goal) # New node

				# Every n iterations bias the RRT
				if iteration%bias_percentage == 0:
					x_rand = x_goal

				iteration += 1

				# Check x_new node collision
				new_collision_free = graph_.is_free(point=x_new, obstacles=obstacles) 
				
				if new_collision_free:
					tree.append(x_new) # Append to the tree the x_new node
					nears.append(x_near) # Append nearest neighbor of x_new

					# Append current node value and place it in the parent list 
					values.append(node_value)
					parent = graph_.generate_parents(values, parent)

					if args.show_random_nodes:
						graph_.draw_random_node(map_=environment_.map)		
					if args.show_new_nodes:
						graph_.draw_new_node(map_=environment_.map, n=x_new)

					graph_.draw_local_planner(p1=x_near, p2=x_new, map_=environment_.map)
					graph_.number_of_nodes = len(tree)
					node_value += 1 # Increment the value for the next randomly generated node

					if graph_.is_goal_reached:
						is_simulation_finished = True
						graph_.parent = parent
						graph_.tree = tree
						graph_.draw_local_planner(p1=x_new, p2=x_goal, map_=environment_.map)
						graph_.path_to_goal()
						graph_.get_path_coordinates()

						if args.path_to_goal:
							graph_.draw_path_to_goal(map_=environment_.map)		

					k += 1 # One more node sampled

		if graph_.is_goal_reached and args.move_robot:
			graph_.draw_trajectory(nears=nears, news=tree, environment=environment_,
				obstacles=obstacles, keep_tree=args.keep_tree)

		pygame.display.update()

	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()