import matplotlib.pyplot as plt
import numpy as np
import math
import pdb

class obstacle_manager():
	def __init__(self, num_obstacles):
		self.circle_obstacles = [] #each entry will be [(location tuple), radius]
		self.gen_circle_obstacles(num_obstacles)
		return self.circle_obstacles #returning this for now, maybe do all collision detection here

	def gen_circle_obstacles(self, num_circles):
		for x in range(num_circles):
			center_point = self.gen_random()
			print("circle at " + str(center_point))
			radius = np.random.rand() * 20 #make this a const max size variable at some point
			print("of radius  " + str(radius))
			circle = plt.Circle(center_point, radius)
			self.ax.add_artist(circle)
			self.circle_obstacles.append([center_point, radius])

	def gen_random(self):
		x_coord = 100 * np.random.rand()
		y_coord = 100 * np.random.rand()
		pick = (x_coord,y_coord)
		return pick

	def euc_dist(self, p1, p2):
		dist = np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))
		return dist

	def collision_detect(self, p1, p2, dist):
		#iterate over all circles if any intersect with new vert, return true
		#we are going to stick pretty close to notation that Paul Bourke uses in his discusion @ http://paulbourke.net/geometry/pointlineplane/
		for x in range(len(self.circle_obstacles)):
			p3 = self.circle_obstacles[x][0] #gets center point
			radius = self.circle_obstacles[x][1]
			print("Circle center at " + str(p3))

			u = ((p3[0] - p1[0]) * (p2[0] - p1[0]) + (p3[1] - p1[1]) * (p2[1] - p1[1]))/np.square(dist)

			x_nearest = p1[0] + u * (p2[0] - p1[0])
			y_nearest = p1[1] + u * (p2[1] - p1[1])
			nearest_point = (x_nearest, y_nearest)

			shortest_dist_to_line = self.euc_dist(nearest_point, p3)

			#if the nearest distance to the line is outside the circle, does not interect
			if shortest_dist_to_line > radius:
				continue #check next circle

			#now if the shortest distance is within the circle, we need to check the end points
			dist_to_p1 = self.euc_dist(p1, p3)
			dist_to_p2 = self.euc_dist(p2, p3)

			if dist_to_p1 > radius and dist_to_p2 > radius:
				continue
			else:
				return true

		return false
