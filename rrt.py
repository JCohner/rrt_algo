import matplotlib.pyplot as plt
import numpy as np
import random

x_array = np.arange(100)
y_array = np.arange(100)

def gen_random():
	x_coord = random.sample(x_array,1)[0]
	y_coord = random.sample(y_array,1)[0]
	pick = (x_coord,y_coord)
	return pick

fig = plt.figure()
plt.plot()
plt.xlim((0,100))
plt.ylim((0,100))
point = gen_random()
plt.scatter(point[0],point[1])
plt.show()