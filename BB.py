#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 14:51:55 2022

@author: Boris Pérez-Cañedo
"""
from munkres import Munkres
from collections import deque
from copy import deepcopy
import sys, time, numbers

def find_subtour(indexes, city=0):
    current = city
    subtour = [current]
    issubtour = False
    i = 0
    while not issubtour:
        if (current, i) in indexes:
            if i in subtour:
                issubtour = True
            else:
                current = i
            subtour.append(i)
        i += 1
        if i>len(indexes):
            i = 0
    return subtour

class Problem:
    def __init__(self, matrix):
        self.matrix = matrix
    def solve(self):
        m = Munkres()
        indexes = m.compute(self.matrix)
        value = 0
        for row, column in indexes:
            value = self.matrix[row][column] + value
        subtour = find_subtour(indexes)
        isfeasible = len(subtour) == len(indexes) + 1
        return (subtour, value, isfeasible,)

class TSP_BB:
    def __init__(self, matrix, max_iter=100, verbose=True, node_class=Problem):
        self.matrix = matrix
        dtype = type(matrix[1][0])
        isnumber = isinstance(dtype(), numbers.Number)
        self.bigM = not isnumber and dtype(*(sys.maxsize,)*len(matrix[1][1]))\
                    or sys.maxsize
        for i in range(len(self.matrix)):
            self.matrix[i][i] = self.bigM 
        self.max_iter = max_iter
        self.verbose = verbose
        self.node_class = node_class
        self.solution = None
        self.incumbent = self.bigM
        self.livenodes = deque()

    def branch(self, p, subtour):
        subproblems = []
        for i in range(len(subtour)-1):
            matrix = deepcopy(p.matrix)
            matrix[subtour[i]][subtour[i+1]] = self.bigM
            for j in range(i):
                aux = matrix[subtour[j]][subtour[j+1]]
                matrix[subtour[j]][:] = [self.bigM]*len(matrix[0])
                matrix[subtour[j]][subtour[j+1]] = aux
            subproblems.append(self.node_class(matrix))
        return subproblems

    def step(self):
        status = ""
        value, subtour, p = self.livenodes.popleft()
        for prob in self.branch(p, subtour):
            tour, value, isfeasible = prob.solve()
            if value < self.incumbent:
                if isfeasible:
                    self.incumbent = value
                    self.solution = tour
                    status = "*IMPROVED*"
                else: self.livenodes.append((value, tour, prob,))
        return status

    def run(self):
        start = time.time()
        try:
            p = self.node_class(self.matrix)
            subtour, value, isfeasible = p.solve()
            if isfeasible:
                self.solution = subtour
                self.incumbent = value
            else: self.livenodes.append((value, subtour, p,))
            i = 1
            while i<=self.max_iter and len(self.livenodes)>0:
                status = self.step()
                if self.verbose:
                    info = (i, len(self.livenodes), self.incumbent, status,)
                    print("Step %d|live nodes %d|best value %s %s"%info)
                i += 1
            if self.verbose:
                if len(self.livenodes)>0:
                    print("Maximum number of iterations reached.")
                else: print("Optimal solution found!")
        except KeyboardInterrupt:
            print("Search interrupted by user.")
        elapsed = time.time()-start
        return len(self.livenodes)>0 and -1 or 1, self.solution,\
                self.incumbent, elapsed

if __name__ == '__main__':
    matrix = [[0, 132, 217, 164, 58],
              [132, 0, 290, 201, 79],
              [217, 290, 0, 113, 303],
              [164, 201, 113, 0, 196],
              [58, 79, 303, 196, 0]]
    tsp = TSP_BB(matrix)
    status, solution, value, elapsed = tsp.run()
    print('tour = ', solution, '\ncost = ', value, '\ntime = ', elapsed)