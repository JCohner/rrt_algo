import matplotlib.pyplot as plt
import numpy as np
import random

class rrt():
	def __init__(self):
		fig = plt.figure()
		plt.plot()
		plt.xlim((0,100))
		plt.ylim((0,100))

	def gen_random(self):
		x_coord = 100 * np.random.rand()
		y_coord = 100 * np.random.rand()
		pick = (x_coord,y_coord)
		return pick

	def plot_point(self, point):
		plt.scatter(point[0],point[1])

	def add_to_tree(self, point):
		self.plot_point(point)
		#return tree

	def run(self, number_points):
		for x in range(number_points):
			point = self.gen_random()
			self.add_to_tree(point)

rrt = rrt()
rrt.run(10)
plt.show()

