#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 19:20:47 2022

@author: Boris Pérez-Cañedo
"""

import numbers
class Lex:
    def __init__(self, *args):
        self.l = list(args)
    def __lt__(self, other):
        if isinstance(other, numbers.Number):
            other = Lex(*(other,)*len(self.l))
        return self.l < other.l
    def __gt__(self, other):
        if isinstance(other, numbers.Number):
            other = Lex(*(other,)*len(self.l))
        return self.l > other.l
    def __getitem__(self, i):
        return self.l[i]
    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            other = Lex(*(other,)*len(self.l))
        return self.l == other.l
    def __le__(self, other):
        return self < other or self == other
    def __ge__(self, other):
        return self > other or self == other
    def __add__(self, other):
        if isinstance(other, numbers.Number):
            other = Lex(*(other,)*len(self.l))
        return Lex(*[self.l[i]+other.l[i] for i in range(len(self.l))])
    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            other = Lex(*(other,)*len(self.l))
        return Lex(*[self.l[i]-other.l[i] for i in range(len(self.l))])
    def __len__(self):
        return len(self.l)
    def __neg__(self):
        return Lex(*[-self.l[i] for i in range(len(self.l))])
    def __str__(self):
        return 'Lex(%s)'%','.join(['%s']*len(self.l)) % tuple(self.l)
    def __repr__(self):
        return 'Lex(%s)'%','.join(['%s']*len(self.l)) % tuple(self.l)