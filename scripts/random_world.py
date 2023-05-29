#!/usr/bin/env python3

import numpy as np
import random as rd

def random_world(n_areas, complex, height=6, width=6):
	"""
		Generate a random world of size height x width with n_areas areas of corrosion.
		Return a list of lists coordinates (x, y) of the corrosion areas with the associated convex polygon.
	"""
	coords = []
	colors = ["Black"]
	f = open("/home/chroma/Downloads/world.urdf", "w")
	for i in range(n_areas):

		x = round(rd.uniform(-width // 2, width // 2), 5)
		y = round(rd.uniform(-height // 2, height // 2), 5)

		redo = True
		while redo:
			if len(coords) == 0:
				redo = False
			for coord in coords:
				if np.sqrt((x - coord[0]) ** 2 + (y - coord[1]) ** 2) < 1.0:
					x = round(rd.uniform(-width // 2, width // 2), 5)
					y = round(rd.uniform(-height // 2, height // 2), 5)
					redo = True
					break
				redo = False

		coords.append([x, y])

		# if i >= n_areas - 3:
		# 	if i >= 10:
		# 		f.write('<xacro:poly3_macro id="' + str(i) + '" color="' + color + '" x="' + str(x) + '" y="' + str(y) + '"/>\n')
		# 	else:
		# 		width = round(rd.uniform(0.05, 0.3), 5)
		# 		height = round(rd.uniform(1.0, 3.0), 5)
		# 		yaw = round(rd.uniform(0.0, 2 * np.pi), 5)
		# 		f.write('<xacro:box_macro id="' + str(i) + '" color="' + color + '" width="' + str(width) + '" length="' + str(height) + '" x="' + str(x) + '" y="' + str(y) + '" yaw="' + str(yaw) + '"/>\n')
		# 	continue


		if complex:
			n_points = rd.randint(2, 7)
		else:
			n_points = 2
		color = rd.choice(colors)

		if n_points == 2:
			radius = round(rd.uniform(0.1, 0.2), 5)
			f.write('<xacro:cylinder_macro id="' + str(i) + '" color="' + color + '" radius="' + str(radius) + '" x="' + str(x) + '" y="' + str(y) + '"/>\n')
		elif n_points == 3:
			f.write('<xacro:poly3_macro id="' + str(i) + '" color="' + color + '" x="' + str(x) + '" y="' + str(y) + '"/>\n')
		elif n_points == 4:
			width = round(rd.uniform(0.05, 0.3), 5)
			height = round(rd.uniform(1.0, 3.0), 5)
			yaw = round(rd.uniform(0.0, 2 * np.pi), 5)
			f.write('<xacro:box_macro id="' + str(i) + '" color="' + color + '" width="' + str(width) + '" length="' + str(height) + '" x="' + str(x) + '" y="' + str(y) + '" yaw="' + str(yaw) + '"/>\n')
		elif n_points == 5:
			f.write('<xacro:poly5_macro id="' + str(i) + '" color="' + color + '" x="' + str(x) + '" y="' + str(y) + '"/>\n')
		elif n_points == 6:
			f.write('<xacro:poly6_macro id="' + str(i) + '" color="' + color + '" x="' + str(x) + '" y="' + str(y) + '"/>\n')
		elif n_points == 7:
			f.write('<xacro:poly7_macro id="' + str(i) + '" color="' + color + '" x="' + str(x) + '" y="' + str(y) + '"/>\n')

	f.close()


if __name__ == '__main__':
	random_world(15, complex=False)
