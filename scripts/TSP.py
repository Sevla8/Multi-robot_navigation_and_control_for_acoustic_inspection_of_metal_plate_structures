#!/usr/bin/env python

import sys
import math
import random
from itertools import combinations
import gurobipy as gp
from gurobipy import GRB


# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        vals = model.cbGetSolution(model._vars)
        # find the shortest cycle in the selected edge list
        tour = subtour(vals)
        if len(tour) < n:
            # add subtour elimination constr. for every pair of cities in tour
            model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2)) <= len(tour)-1)


# Given a tuplelist of edges, find the shortest subtour
def subtour(vals):
    # make a list of edges selected in the solution
    edges = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
    unvisited = list(range(n))
    cycle = range(n+1)  # initial length has 1 more city
    while unvisited:  # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*') if j in unvisited]
        if len(cycle) > len(thiscycle):
            cycle = thiscycle
    return cycle

n = 12

points = [
    (-0.7999999999999998, -2.05),
	(1.0250000000000004, -2.025),
	(2.2, -2.025),
	(-0.7999999999999998, -0.7999999999999998),
	(1.0250000000000004, -0.7749999999999999),
	(2.2, -0.7749999999999999),
	(-0.8249999999999997, 0.42500000000000027),
	(1.0, 0.4750000000000001),
	(2.1750000000000007, 0.4750000000000001),
	(-0.8249999999999997, 2.0500000000000007),
	(1.0, 2.1000000000000005),
	(2.1750000000000007, 2.1000000000000005)
]

print(f'points: {points}')

# Dictionary of Euclidean distance between each pair of points
dist = {(i, j): math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2))) for i in range(n) for j in range(i)}

m = gp.Model()

# Create variables
vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i, j in vars.keys():
    vars[j, i] = vars[i, j]  # edge in opposite direction

# Add degree-2 constraint
m.addConstrs(vars.sum(i, '*') == 2 for i in range(n))

# Optimize model
m._vars = vars
m.Params.LazyConstraints = 1
m.optimize(subtourelim)

vals = m.getAttr('X', vars)
tour = subtour(vals)
assert len(tour) == n

print('')
print('Optimal tour: %s' % str(tour))
print('Optimal cost: %g' % m.ObjVal)
print('')