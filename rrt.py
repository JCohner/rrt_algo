import matplotlib.pyplot as plt
import numpy as np
import pdb
from pprint import pprint

NODE = 0
CHILD_LIST = 1
PARENT = 2

#plt.ion()
class rrt():
	def __init__(self):
		fig = plt.figure()
		plt.plot()
		plt.xlim((0,100))
		plt.ylim((0,100))
		self.vertex_list = []
		self.delta = 10 #unit step
		
		#gen, plot, and to to list our root!
		first_point = self.gen_random()
		print("root is at " + str(first_point))
		self.vertex_list.append([first_point, [], None])
		self.plot_point(first_point, None)

	def add_to_vertex_list(self, point):
		nearest_vertex, dist = self.nearest_vertex(point)
		new_vert = self.unit_step_to_nearest_vertex(point, nearest_vertex, dist)
		#add this new vert as a child of the nearest vert
		
		for x in range(len(self.vertex_list)):
			if (self.vertex_list[x][0] == nearest_vertex):
				self.vertex_list[x][1].append(new_vert)
		self.vertex_list.append([new_vert, [], nearest_vertex])
		#pdb.set_trace()
		self.plot_point(new_vert, nearest_vertex)

	def unit_step_to_nearest_vertex(self, point, vertex, dist):
		x_delta = point[0] - vertex[0] 
		y_delta = point[1] - vertex[1]
		print("closest vertex to theor point " + str(point) + " determined as vertex " + str(vertex))

		vector = np.array([x_delta, y_delta])
		print("vector is " + str(vector))
		norm_vector = vector / dist
		print("norm vector is " + str(norm_vector))
		unit_vector = (norm_vector * self.delta).tolist()
		new_vert = (vertex[0] + unit_vector[0], vertex[1] + unit_vector[1])
		print("new vertice should be placed at " + str(new_vert))
		return new_vert

	def gen_random(self):
		x_coord = 100 * np.random.rand()
		y_coord = 100 * np.random.rand()
		pick = (x_coord,y_coord)
		return pick

	def plot_point(self, point, parent):
		if (parent == None):
			plt.scatter(point[0],point[1])
		else:
			plt.plot([point[0],parent[0]], [point[1],parent[1]], '-o')

	def nearest_vertex(self,point):
		#set min distance to infinite
		min_dist = np.inf
		min_pt = None
		print("finding closest vertex to theoretical point " + str(point))
		for x in range(len(self.vertex_list)):
			print("checking point " + str(self.vertex_list[x][0]))
			#pdb.set_trace()
			dist = np.sqrt(np.square(point[0] - self.vertex_list[x][0][0]) + np.square(point[1] - self.vertex_list[x][0][1]))
			print("dist is " + str(dist))
			if (dist < min_dist):
				print("new min dist set as " + str(dist))
				min_dist = dist
				min_pt = self.vertex_list[x][0]
		print("determined closest point is " + str(min_pt))
		return min_pt, min_dist


	def run(self, number_points):
		for x in range(number_points):
			#genrate the random point
			point = self.gen_random()
			#calculate nearest existing vertex, add point to vertex list			
			self.add_to_vertex_list(point)

#pdb.set_trace()
rrt = rrt()
rrt.run(20)
pprint(rrt.vertex_list)
#pdb.set_trace()
plt.show()

