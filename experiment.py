#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 21:52:51 2022

@author: Boris Pérez-Cañedo
"""

from tfn import TFN
from lex import Lex
from twoOpt import run_2opt
from tools import load_cost_matrix
import random2

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

N = 1000 # Number of trials
optimum = TFN(777.0,989.0,1265.0)
target = Lex(f1(optimum),f2(optimum),f3(optimum))
attempts = 100 # Change this to 10, 20, ..., 100 to reproduce the article results.
success = 0

random2.seed(42) # For reproducibility
for i in range(N):
    solution, value, elapsed = run_2opt(lexC, attempts)
    success += value == target
print("2-opt with lexicographic ranking, probability of success: ", success/N)
    
success = 0
random2.seed(42) # For reproducibility
for i in range(N):
    solution, value, elapsed = run_2opt(rC, attempts)
    success += value == target
print("2-opt with ranking function, probability of success: ", success/N)

success_lex = 0
success_lin = 0
for i in range(N):
    random2.seed(i) # For reproducibility
    solution1, value1, elapsed1 = run_2opt(lexC, attempts)
    random2.seed(i) # For reproducibility
    solution2, value2, elapsed2 = run_2opt(rC, attempts)
    success_lex += value1 < value2
    success_lin += value1 > value2
print("lex criterion, outperform probability:", success_lex/N)
print("linear ranking,  outperform probability:", success_lin/N)