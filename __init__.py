#!/usr/bin/env python
#-*- coding: utf-8 -*-

import cmath as c
from math import *

i = 1j

def Int(f, a, b, n=10000):
    """Return int_a^b f(t)dt with the trapezoidal rule."""
    x = a
    dx = (b-a) / n
    I = 0
    for k in range(n):
        I = I + 0.5 * (f(x+dx) + f(x)) * dx
        x = x + dx
    return I
