import matplotlib.pyplot as plt
import numpy as np
import random
import pdb
from pprint import pprint
#plt.ion()
class rrt():
	def __init__(self):
		fig = plt.figure()
		plt.plot()
		plt.xlim((0,100))
		plt.ylim((0,100))
		self.vertex_list = []
		self.delta = 1 #unit step
		
		#gen, plot, and to to list our root!
		first_point = self.gen_random()
		print("root is at " + str(first_point))
		self.vertex_list.append([first_point, []])
		self.plot_point(first_point)

	def add_to_vertex_list(self, point):
		nearest_vertex = self.nearest_vertex(point)
		new_vert = self.unit_step_to_nearest_vertex(point, nearest_vertex)
		#add this new vert as a child of the nearest vert
		for x in range(len(self.vertex_list)):
			if (self.vertex_list[x][0] == nearest_vertex):
				self.vertex_list[x][1].append(new_vert)
		self.vertex_list.append([new_vert, []])
		self.plot_point(new_vert)

	def unit_step_to_nearest_vertex(self, point, vertex):
		x_delta = point[0] - vertex[0]
		y_delta = point[1] - vertex[1]

		angle = np.arctan(y_delta/x_delta)
		#pdb.set_trace()
		new_x = (vertex[0] + np.cos(angle)) * self.delta
		new_y = (vertex[1] + np.sin(angle)) * self.delta

		new_vert = (new_x, new_y)
		self.plot_point(new_vert)
		#print("vertex that is a unit step away is " + str(new_vert))
		return new_vert

	def gen_random(self):
		x_coord = 100 * np.random.rand()
		y_coord = 100 * np.random.rand()
		pick = (x_coord,y_coord)
		return pick

	def plot_point(self, point):
		plt.scatter(point[0],point[1])

	def nearest_vertex(self,point):
		#set min distance to infinite
		min_dist = np.inf
		min_pt = None
		print("point is " + str(point))
		for x in range(len(self.vertex_list)):
			#print("check vs point " + str(self.vertex_list[x][0]))
			dist = np.sqrt(np.square(point[0] - self.vertex_list[x][0][0])+ np.square(np.square(point[1] - self.vertex_list[x][0][1])))
			if (dist < min_dist):
				min_dist = dist
				min_pt = self.vertex_list[x][0]
		#print("nearest vertex is " + str(min_pt))
		return min_pt


	def run(self, number_points):
		for x in range(number_points):
			#genrate the random point
			point = self.gen_random()
			#calculate nearest existing vertex, add point to vertex list			
			self.add_to_vertex_list(point)
#pdb.set_trace()
rrt = rrt()
rrt.run(100)
pprint(rrt.vertex_list)
#pdb.set_trace()
plt.show()

