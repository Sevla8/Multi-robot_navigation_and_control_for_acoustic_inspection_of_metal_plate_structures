#!/usr/bin/env python3

import cv2 as cv
import os as os

def get_Kappa_coefficient(template, image):
	if template.shape != image.shape:
		print("Images must have the same size")
		return
	l, w, _ = template.shape
	TN = 0
	TP = 0
	FN = 0
	FP = 0
	unmatched0 = 0
	unmatched1 = 0
	unmatched2 = 0
	for i in range(l):
		for j in range(w):
			if template[i, j, 0] != 0 or template[i, j, 1] != 0 or template[i, j, 2] != 0: # empty
				if image[i, j, 0] == 255 and image[i, j, 1] == 255 and image[i, j, 2] == 255: # empty
					TN += 1
				elif image[i, j, 0] == 0 and image[i, j, 1] == 0 and image[i, j, 2] == 255: # corrosion
					FP += 1
				else:
					unmatched0 += 1
			elif template[i, j, 0] == 0 and template[i, j, 1] == 0 and template[i, j, 2] == 0: # corrosion
				if image[i, j, 0] == 255 and image[i, j, 1] == 255 and image[i, j, 2] == 255: # empty
					FN += 1
				elif image[i, j, 0] == 0 and image[i, j, 1] == 0 and image[i, j, 2] == 255: # corrosion
					TP += 1
				else:
					unmatched1 += 1
			else:
				unmatched2 += 1
	print("TP: ", TP, "TN: ", TN, "FP: ", FP, "FN: ", FN, "Unmatched0: ", unmatched0, "Unmatched1: ", unmatched1, "Unmatched2: ", unmatched2)
	f_c = ((TN + FN) * (TN + FP) + (FP + TP) * (FN + TP)) / (TP + TN + FN +FP)
	kappa = (TP + TN - f_c) / ((TP + TN + FN + FP) - f_c)
	return kappa, unmatched0 + unmatched1 + unmatched2

def get_scores(world, path):
	template = cv.imread(f'../graphics/{world}.png')
	template = cv.resize(template, (120, 120))
	template = cv.flip(template, 1)
	template = cv.rotate(template, cv.ROTATE_90_CLOCKWISE)
	template = cv.rotate(template, cv.ROTATE_90_CLOCKWISE)

	image = cv.imread(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}/occupancy_grid.png')
	image = cv.resize(image, (120, 120))

	kappa, _ = get_Kappa_coefficient(template, image)
	print(f'Kappa coefficient: {kappa}')

	word = 'completed'
	with open(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}/crawler_navigation_nospawn.out', 'r') as file:
		for line in file:
			if word in line:
				# get time which is 1 word after word
				time = line.split()[line.split().index(word) + 2]
				time = float(time)
				break

	result_file = open(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/results.txt', 'a')
	result_file.write(f'{path} {kappa:.2f} {time:.2f}\n')
	result_file.close()

	image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
	both = cv.addWeighted(template, 0.5, image, 0.5, 0)
	cv.imwrite(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}/both.png', both)

if __name__ == '__main__':
	if os.path.isfile('/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/results.txt'):
		os.remove('/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/results.txt')

	GRID_WIDTH = 6
	GRID_HEIGHT = 6
	GRID_RESOLUTION = 0.05
	DISTANCE = [6.0, 3.0, 2.0, 1.0]
	OVERLAP = 0.1
	STRIDE = [1.0, 2.0, 3.0, 6.0]
	N_POINTS = [3, 4, 5, 7, 10]
	N_CRAWLERS = [2, 3, 4]
	WORLD = [
		'test_model_05_1', 'test_model_05_2', 'test_model_05_3', 'test_model_05_4', 'test_model_05_5',
		'test_model_8_1', 'test_model_8_2', 'test_model_8_3', 'test_model_8_4', 'test_model_8_5',
		'test_model_11_1', 'test_model_11_2', 'test_model_11_3', 'test_model_11_4', 'test_model_11_5',
		'test_model_15_1', 'test_model_15_2', 'test_model_15_3', 'test_model_15_4', 'test_model_15_5',
		'test_model_20_1',
		'test_model_30_1',
		'test_model_11_complex_1',
		'test_model_15_complex_1'
	]
	MISSION = [
		'peinture_au_rouleau',
		'ski_nordique',
		'investigation_polygonale'
	]

	for mission in MISSION:
		if mission == 'peinture_au_rouleau':
			for world in WORLD:
				for distance in DISTANCE:
					path = f'{mission}-{world}-{distance}'
					if os.path.isdir(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}') and os.path.isfile(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}/occupancy_grid.png'):
						get_scores(world, path)
						print(f'OK {path}')
					else:
						print(f'{path} does not exist')
		elif mission == 'ski_nordique':
			for world in WORLD:
				for distance in DISTANCE:
					for stride in STRIDE:
						path = f'{mission}-{world}-{distance}-{stride}'
						if os.path.isdir(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}') and os.path.isfile(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}/occupancy_grid.png'):
							get_scores(world, path)
							print(f'OK {path}')
						else:
							print(f'{path} does not exist')
		elif mission == 'investigation_polygonale':
			for world in WORLD:
				for point in N_POINTS:
					for crawler in N_CRAWLERS:
						for distance in DISTANCE:
							path = f'{mission}-{world}-{point}-{crawler}-{distance}'
							if os.path.isdir(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}') and os.path.isfile(f'/home/chroma/Documents/Multi-robot_navigation_and_control_for_acoustic_inspection_of_metal_plate_structures/tests/{path}/occupancy_grid.png'):
								get_scores(world, path)
								print(f'OK {path}')
							else:
								print(f'{path} does not exist')

