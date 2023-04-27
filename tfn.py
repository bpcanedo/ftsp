#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 19:19:26 2022

@author: Boris Pérez-Cañedo
"""

import numbers
class TFN:
    def __init__(self, a=0, b=0, c=0):
        assert a<=b and b<=c, 'not a valid triangular fuzzy number'
        self.a, self.b, self.c = a, b, c
    def __add__(self, other):
        if isinstance(other, numbers.Number):
            other = TFN(other, other, other)
        return TFN(self.a+other.a, self.b+other.b, self.c+other.c)
    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            other = TFN(other, other, other)
        return TFN(self.a-other.c, self.b-other.b, self.c-other.a)        
    def __neg__(self):
        return TFN(-self.c, -self.b, -self.a)
    def __str__(self):
        return 'TFN(%s,%s,%s)' % (self.a, self.b, self.c,)
    def __repr__(self):
        return 'TFN(%s,%s,%s)' % (self.a, self.b, self.c,)