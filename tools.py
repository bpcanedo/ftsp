#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 22:39:47 2022

@author: Boris Pérez-Cañedo
"""

from tfn import TFN
import csv
from ast import literal_eval
def load_cost_matrix(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        C = [[TFN(*literal_eval(cell)) for cell in row] for row in reader]
        return C

def fuzzy_value(c, sol):
    value = TFN()
    for i in range(len(sol)-1):
        value += c[sol[i]][sol[i+1]]
    return value
       
    