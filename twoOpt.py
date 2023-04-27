#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  6 23:34:47 2022

@author: Boris Pérez-Cañedo
"""
import random2, sys, time

def two_opt(matrix, route):
    # Modified code from http://pedrohfsd.com/2017/08/09/2opt-part1.html
    best = route
    best_value = cost(matrix, best)
    improved = True
    while improved:
         improved = False
         for i in range(1, len(route)-2):
              for j in range(i+1, len(route)):
                   if j-i == 1: continue
                   new_route = route[:]
                   new_route[i:j] = route[j-1:i-1:-1]
                   value = cost(matrix, new_route)
                   if value < best_value:
                        best = new_route
                        best_value = value
                        improved = True
         route = best
    return best, best_value
 
def random_route(ncities):
    return [0] + random2.sample(range(1, ncities), ncities - 1) + [0]

def run_2opt(matrix, max_iter):
    start = time.time()
    ncities = len(matrix)
    best = None
    value = sys.maxsize
    i = 1
    while i <= max_iter:
        initial = random_route(ncities)
        new_sol, new_value = two_opt(matrix, initial)
        if new_value < value:
            best = new_sol
            value = new_value
        i += 1
    elapsed = time.time() - start
    return best, value, elapsed

def cost(matrix, route):
    value = 0
    for i in range(len(route)-1):
        value = matrix[route[i]][route[i+1]] + value
    return value

if __name__ == '__main__':
    # Example br17 from http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/ATSP.html
    matrix = [[9999,3,5,48,48,8,8,5,5,3,3,0,3,5,8,8,5],
         [3,9999,3,48,48,8,8,5,5,0,0,3,0,3,8,8,5],
         [5,3,9999,72,72,48,48,24,24,3,3,5,3,0,48,48,24],
         [48,48,74,9999,0,6,6,12,12,48,48,48,48,74,6,6,12],
         [48,48,74,0,9999,6,6,12,12,48,48,48,48,74,6,6,12],
         [8,8,50,6,6,9999,0,8,8,8,8,8,8,50,0,0,8],
         [8,8,50,6,6,0,9999,8,8,8,8,8,8,50,0,0,8],
         [5,5,26,12,12,8,8,9999,0,5,5,5,5,26,8,8,0],
         [5,5,26,12,12,8,8,0,9999,5,5,5,5,26,8,8,0],
         [3,0,3,48,48,8,8,5,5,9999,0,3,0,3,8,8,5],
         [3,0,3,48,48,8,8,5,5,0,9999,3,0,3,8,8,5],
         [0,3,5,48,48,8,8,5,5,3,3,9999,3,5,8,8,5],
         [3,0,3,48,48,8,8,5,5,0,0,3,9999,3,8,8,5],
         [5,3,0,72,72,48,48,24,24,3,3,5,3,9999,48,48,24],
         [8,8,50,6,6,0,0,8,8,8,8,8,8,50,9999,0,8],
         [8,8,50,6,6,0,0,8,8,8,8,8,8,50,0,9999,8],
         [5,5,26,12,12,8,8,0,0,5,5,5,5,26,8,8,999]]
    solution, value, elapsed = run_2opt(matrix, 1000)
    print('tour = ', solution, '\ncost = ', value, '\ntime = ', elapsed)