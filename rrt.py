import matplotlib.pyplot as plt
import numpy as np
import math
import pdb
from pprint import pprint
import os

import obstacle

NODE = 0
CHILD_LIST = 1
PARENT = 2


#plt.ion() #enable this during debugging to see real time 
class rrt():
	def __init__(self):
		fig, self.ax = plt.subplots()
		plt.plot()
		plt.xlim((0,100))
		plt.ylim((0,100))
		self.vertex_list = []
		self.win_node = None
		self.delta = 1 #unit step
		
		#randomize seed
		np.random.seed(int(np.random.rand()*1000))

		#instantiate the obstacle manager
		self.ob_man = obstacle.obstacle_manager(20, self.ax)

		#add goal to map
		self.plant_goal()
		#add root node
		self.plant_root()

	def plant_root(self):
		root = self.gen_random()
		conflict = True
		while(conflict):
			conflict = self.ob_man.init_collision_detect(root)
			if conflict:
				root = self.gen_random()
		self.root = root
		self.vertex_list.append([root, [], None])
		self.plot_point(root, None)
		#check if root has a straight path to winning
		win_con = self.ob_man.win_check(self.root, self.goal)
		if not win_con:
			#perform affirtmative win condition tasks
			self.win_node = self.root
			self.add_to_vertex_list(self.goal, self.win_node)
		

	def plant_goal(self):
		goal = self.gen_random()
		conflict = True
		while(conflict):
			conflict = self.ob_man.init_collision_detect(goal)
			if conflict:
				goal = self.gen_random()

		self.goal = goal
		self.plot_point(goal, None)

	def add_to_vertex_list(self, new_vert, nearest_vertex):
		#add this new vert as a child of the nearest vert
		for x in range(len(self.vertex_list)):
			if (self.vertex_list[x][0] == nearest_vertex):
				self.vertex_list[x][1].append(new_vert)
		self.vertex_list.append([new_vert, [], nearest_vertex])
		
		self.plot_point(new_vert, nearest_vertex)
		#pprint(self.vertex_list)
		#pdb.set_trace()

	def unit_step_to_nearest_vertex(self, point, vertex, dist):
		x_delta = point[0] - vertex[0] 
		y_delta = point[1] - vertex[1]

		vector = np.array([x_delta, y_delta])
		norm_vector = vector / dist
		unit_vector = (norm_vector * self.delta).tolist()
		new_vert = (vertex[0] + unit_vector[0], vertex[1] + unit_vector[1])

		return new_vert

	def gen_random(self):
		x_coord = 100 * np.random.rand()
		y_coord = 100 * np.random.rand()
		pick = (x_coord,y_coord)
		return pick

	def plot_point(self, point, parent):
		if (parent == None):
			if (point == self.goal):
				print("plotting goal at: " + str(self.goal))
				plt.scatter(point[0],point[1], color = 'yellow', marker = 'X', s=200)
			elif (point == self.root):
				print("plotting root at: " + str((point[0],point[1])))
				plt.scatter(point[0],point[1], color = 'red', marker = 'P', s=200)
		else:
			plt.plot([point[0],parent[0]], [point[1],parent[1]], '-ob')

	def nearest_vertex(self,point):
		#set min distance to infinite
		min_dist = np.inf
		min_pt = None
		for x in range(len(self.vertex_list)):
			dist = np.sqrt(np.square(point[0] - self.vertex_list[x][0][0]) + np.square(point[1] - self.vertex_list[x][0][1]))
			if (dist < min_dist):
				min_dist = dist
				min_pt = self.vertex_list[x][0]
		return min_pt, min_dist

	def recurse_win(self, node):
		self.win_path.append(node)
		#get the nodes parent
		for x in range(len(self.vertex_list)):
			if node == self.vertex_list[x][0]:
				parent = self.vertex_list[x][2]
				break
		self.plot_win_tree(node, parent)
		if parent == self.root:
			return
		else:
			self.recurse_win(parent)

	def plot_win_tree(self, node, parent):
		plt.plot([node[0],parent[0]], [node[1],parent[1]], '-oy')

	def run(self, number_points):
		missed = 0
		for x in range(number_points):
			#genrate the random point
			point = self.gen_random()
			#calculate nearest existing vertex			
			nearest_vertex, dist = self.nearest_vertex(point)
			#take a unit step in the direction of the random point to find the new vertice to add
			new_vert = self.unit_step_to_nearest_vertex(point, nearest_vertex, dist)
			collis_bool = self.ob_man.collision_detect(nearest_vertex, new_vert, self.delta)
			#if that new vertice does not collide with an obstacle then we can add it to the vertex list
			if not collis_bool:
				self.add_to_vertex_list(new_vert, nearest_vertex)
				#check win condition
				win_con = self.ob_man.win_check(nearest_vertex, self.goal)
				if not win_con:
					#perform affirtmative win condition tasks
					self.win_node = new_vert
					self.add_to_vertex_list(self.goal, self.win_node)
					break

			else:
				#on miss add to miss count, recurse over count so we still have requested number of nodes
				missed = missed + 1
		print("in total " + str(missed) + " misses generated")
		if missed != 0 and self.win_node == None:
			self.run(missed)

		if self.win_node == None:
			print("no path to goal found")
		else:
			self.win_path = []
			self.recurse_win(self.goal)

rrt = rrt()
if (rrt.win_node == rrt.root):
	print("root had a straight path to our goal!")
else:
	rrt.run(500)
#pdb.set_trace()
#pprint(rrt.vertex_list)
plt.title("RRT with Obstacles")
plt.scatter(rrt.root[0], rrt.root[1], color = 'red', marker = 'P', s=200, zorder = 100)
filename = 'pictures/{}.png'.format(len(os.listdir('pictures')))
plt.savefig(filename)
plt.show()


