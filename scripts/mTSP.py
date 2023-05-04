#!/usr/bin/env python

import numpy as np
from oct2py import octave
from math import sqrt

octave.addpath('/home/chroma/Documents/CS-7000_Master-Thesis/')
octave.eval('pkg load statistics')
XY = np.array([
	[1150.0, 1760.0],
	[630.0, 1660.0],
	[40.0, 2090.0],
	[750.0, 1100.0],
	[750.0, 2030.0],
	[1030.0, 2070.0],
	[1650.0, 650.0],
	[1490.0, 1630.0],
	[790.0, 2260.0],
	[710.0, 1310.0],
	[840.0, 550.0],
	[1170.0, 2300.0],
	[970.0, 1340.0],
	[510.0, 700.0],
	[750.0, 900.0],
	[1280.0, 1200.0],
	[230.0, 590.0],
	[460.0, 860.0],
	[1040.0, 950.0],
	[590.0, 1390.0],
	[830.0, 1770.0],
	[490.0, 500.0],
	[1840.0, 1240.0],
	[1260.0, 1500.0],
	[1280.0, 790.0],
	[490.0, 2130.0],
	[1460.0, 1420.0],
	[1260.0, 1910.0],
	[360.0, 1980.0]
])
max_salesmen = 5
depots = np.array([
    [1150.0, 1760.0],
	[630.0, 1660.0],
	[40.0, 2090.0],
	[750.0, 1100.0],
	[750.0, 2030.0]
])
CostType = 1
MIN_TOUR = 1
POP_SIZE = 256
NUM_ITER = 100
SHOW_PROG = True
SHOW_RES = True
# DMAT = np.array([
#     [0, sqrt((0-5)**2 + (0-0)**2), sqrt((0-5)**2 + (0-4)**2), sqrt((0-8)**2 + (0-2)**2)],
# 	[sqrt((5-0)**2 + (0-0)**2), 0, sqrt((5-5)**2 + (0-4)**2), sqrt((5-8)**2 + (0-2)**2)],
# 	[sqrt((4-0)**2 + (5-0)**2), sqrt((4-5)**2 + (5-0)**2), 0, sqrt((4-8)**2 + (5-2)**2)],
# 	[sqrt((2-0)**2 + (8-0)**2), sqrt((2-5)**2 + (8-0)**2), sqrt((2-4)**2 + (8-5)**2), 0]
# ])
[min_dist, best_tour, generation] = octave.mdmtspv_ga(XY, max_salesmen, depots, CostType, MIN_TOUR, POP_SIZE, NUM_ITER, SHOW_PROG, SHOW_RES, nout=3)
print("Minimum distance: ")
print(min_dist)
print("Best tour: ")
print(best_tour)
print("Generation: ")
print(generation)