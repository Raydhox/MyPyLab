#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Fun:

    def __init__(self, f, fx="f"):
        """Create a function Fun where:
f = lambda x : f(x)
fx is a string which represents f(x)."""
        self.f = f
        self.fx = fx

    def __repr__(self):
        return self.fx

##    def __eq__(self, g):
##        """???"""
##        pass

    #===Operations===
    def __add__(self, g):
        """Return the function f+g, f is the current function."""
        return Fun( lambda x : self(x) + g(x) )

    def __sub__(self, g):
        """Return the function f-g, f is the current function."""
        return Fun( lambda x : self(x) - g(x) )

    def __rmul__(self, k):
        """K is a real or a complex. Return the function k*f, f is the current function."""
        if type(k) in [int, float, complex]:
            return Fun( lambda x : k*self(x) )

    def __mul__(self, Q):
        """Return the function f*g, f is the current function."""
        return Fun( lambda x : self(x) * g(x) )

    def __truediv__(self, Q):
        """Return the function f/g, f is the current function."""
        return Fun( lambda x : self(x) * g(x) )

    def __pow__(self, n):
        """Return the function fofofo...of, f is the current function."""
        #Function f^n (x) = (fofo...of)(x)
        def fn(f, n, x):
            y = x
            for k in range(n):
                y = f(y)
            return y
        return Fun( lambda x: fn(self.f, n, x)) )

    def __call__(self, Q):
        """Return the function fof,  f is the current function."""
        return Fun( lambda x : self(self)(x) )

if __name__ == "__main__" :
    f = Fun(lambda x : x**2)
