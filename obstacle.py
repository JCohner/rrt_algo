import matplotlib.pyplot as plt
import numpy as np
import math
import pdb

class obstacle_manager():
	def __init__(self, num_obstacles, ax):
		self.circle_obstacles = [] #each entry will be [(location tuple), radius]
		self.ax = ax
		self.gen_circle_obstacles(num_obstacles)
		return  #returning this for now, maybe do all collision detection here

	def gen_circle_obstacles(self, num_circles):
		for x in range(num_circles):
			center_point = self.gen_random()
			radius = np.random.rand() * 20 #make this a const max size variable at some point
			circle = plt.Circle(center_point, radius, color = 'k')
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

	#call when plotting root of circle to ensure that it doesnt start in an obstacles
	def init_collision_detect(self, p1):
		for x in range(len(self.circle_obstacles)):
			circle_cent = self.circle_obstacles[x][0]
			radius = self.circle_obstacles[x][1]
			dist_from_root = self.euc_dist(p1, circle_cent)

			if dist_from_root < radius:
				return True
			else:
				continue
		return False

	def collision_detect(self, p1, p2, dist):
		#iterate over all circles if any intersect with new vert, return true
		#we are going to stick pretty close to notation that Paul Bourke uses in his discusion @ http://paulbourke.net/geometry/pointlineplane/
		for x in range(len(self.circle_obstacles)):
			
			p3 = self.circle_obstacles[x][0] #gets center point
			#pdb.set_trace()
			radius = self.circle_obstacles[x][1]

			u = ((p3[0] - p1[0]) * (p2[0] - p1[0]) + (p3[1] - p1[1]) * (p2[1] - p1[1]))/np.square(dist)
			#u is already telling us if the point exists on the line segment or not, with abs(u) > 1 meaning that it does not


			x_nearest = p1[0] + u * (p2[0] - p1[0]) #1 + u seems to adjust correctly
			y_nearest = p1[1] + u * (p2[1] - p1[1])
			nearest_point = (x_nearest, y_nearest)

			shortest_dist_to_line = self.euc_dist(nearest_point, p3)
			#if the nearest distance to the line is outside the circle, does not interect
			if shortest_dist_to_line > radius:
				#if the shortest distance to the line lies outisde of the circle, it cannot intersect therefore we can check the next circle obstacle
				continue 
			#pdb.set_trace()
			#shortest distance to line within the circle, we need to check which of three cases
			#Case 1: one of the end points exists within the circle INTERSECT CASE
			#Case 2: both points lay outside circle
				#2a: shortest point to line exists within circle, but line segment does not intersect circle NO-INTERSECT CASE
				#2b: shortest point to line exists within circle, and line segment intersects with circle -> this means that shortest point to circle exists on line segment INTERSECT CASE

			dist_to_p1 = self.euc_dist(p1, p3)
			dist_to_p2 = self.euc_dist(p2, p3)

			# print("dist to p1: " + str(dist_to_p1))
			# print("dist_to_p2: " + str(dist_to_p2))
			# print("radius of current cicle: " + str(radius))

			if dist_to_p1 > radius and dist_to_p2 > radius:
				#print("both points outside of circle, checking if closest point lies on line")
				#check if p3 exists on line, else continue
				if u < 1 and u > 0:
					#this means that the shortest point to the circle exists on the line and is within the circle, therefore the line intersects with the circle
					return True
				else:
					continue
			else:
				#one of the points is within the line
				#print("one of the points exists within circle")
				return True

		return False

	def win_check(self, vert, goal):
		#pdb.set_trace()
		dist = self.euc_dist(vert, goal)
		win_con = self.collision_detect(vert, goal, dist)
		return win_con