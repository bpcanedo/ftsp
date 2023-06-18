#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 21:52:51 2022

@author: Boris Pérez-Cañedo
"""

import csv
from lex import Lex
from BB import TSP_BB
from twoOpt import run_2opt
from tools import load_cost_matrix, fuzzy_value
import random

# Lexicographic ranking criterion
f1 = lambda fn:(fn.a+2*fn.b+fn.c)/4
f2 = lambda fn:fn.b
f3 = lambda fn:fn.c-fn.a

C = load_cost_matrix('cost.csv')
lexC = [[Lex(f1(c),f2(c),f3(c))
        for c in row]
        for row in C]
rC = [[f1(c) for c in row]
             for row in C]

# Find an optimal solution
tsp = TSP_BB(lexC, verbose=True) 
_, solution, _, _ = tsp.run()
optimum = fuzzy_value(C, solution)
print(optimum)

target = Lex(f1(optimum),f2(optimum),f3(optimum))

N = 1000 # Number of trials

# Success probability and execution time analysis

data_success_prob = [['Lexicographic criterion', 'Linear ranking function']]
data_outperformance_prob = [['Lexicographic criterion', 'Linear ranking function']]
data_exec_time = [['Lexicographic criterion', 'Linear ranking function']]

for attempts in range(10, 110, 10):
    success_lex = 0
    total_time_lex = 0
    random.seed(42) # For reproducibility
    for i in range(N):
        solution, value, time_lex = run_2opt(lexC, attempts)
        success_lex += value == target
        total_time_lex += time_lex
    print("2-opt with lexicographic ranking, probability of success: ", success_lex/N)
    print("2-opt with lexicographic ranking, avg. execution time: ", total_time_lex/N)

        
    success_lin = 0
    total_time_lin = 0
    random.seed(42) # For reproducibility
    for i in range(N):
        solution, value, time_lin = run_2opt(rC, attempts)
        f_value = fuzzy_value(C, solution)
        success_lin += Lex(f1(f_value),f2(f_value),f3(f_value)) == target
        total_time_lin += time_lin
    print("2-opt with ranking function, probability of success: ", success_lin/N)
    print("2-opt with ranking function, avg. execution time: ", total_time_lin/N)
    data_success_prob.append([success_lex/N, success_lin/N])
    data_exec_time.append([total_time_lex/N, total_time_lin/N])
    
    # Outperformance probability analysis
    
    success_lex = 0
    success_lin = 0
    for i in range(N):
        random.seed(i) # For reproducibility
        solution1, lex_val1, elapsed1 = run_2opt(lexC, attempts)
        random.seed(i) # For reproducibility
        solution2, r_val, elapsed2 = run_2opt(rC, attempts)
        f_value = fuzzy_value(C, solution2)
        lex_val2 = Lex(f1(f_value),f2(f_value),f3(f_value))
        success_lex += lex_val1 < lex_val2
        success_lin += lex_val1 > lex_val2
    print("lex criterion, outperform probability:", success_lex/N)
    print("linear ranking, outperform probability:", success_lin/N)
    data_outperformance_prob.append([success_lex/N, success_lin/N])

with open('success_prob.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_success_prob)

with open('exec_time.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_exec_time)

with open('outperformance_prob.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_outperformance_prob)
