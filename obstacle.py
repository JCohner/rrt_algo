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

	def collision_detect(self, vector):