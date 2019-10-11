#!/usr/bin/env python
#-*- coding: utf-8 -*-

class Fun:

    def __init__(self, function, name="f"):
        """Create a function Fun where:
f = lambda x : f(x)
fx is a string which represents f(x)."""
        self.function = function
        self.name = name
        
    def __repr__(self):
        return "Fun: x |--> %s(x)" %(self.name)

    #===Operations===
    def __add__(self, g):
        """Return the function f+g, f is the current function."""
        name = "(%s + %s)" %(self.name, g.name)
        return Fun( lambda x : self(x) + g(x), name )

    def __sub__(self, g):
        """Return the function f-g, f is the current function."""
        name = "(%s - %s)" %(self.name, g.name)
        return Fun( lambda x : self(x) - g(x), name )

    def __rmul__(self, k):
        """K is a real or a complex. Return the function k*f, f is the current function."""
        if type(k) in [int, float, complex]:
            name = "{}{}".format(k, self.name)
            return Fun( lambda x : k*self(x), name )

    def __mul__(self, g):
        """Return the function f*g, f is the current function."""
        name = "(%s * %s)" %(self.name, g.name)
        return Fun( lambda x : self(x) * g(x), name )

    def __truediv__(self, g):
        """Return the function f/g, f is the current function."""
        name = "(%s / %s)" %(self.name, g.name)
        return Fun( lambda x : self(x) / g(x), name )

    def __pow__(self, n):
        """Return the function fofofo...of, f is the current function."""
        #Function f^n (x) = (fofo...of)(x)
        def fn(f, n, x):
            y = x
            for k in range(n):
                y = f(y)
            return y
        name = "%s^(%d)" %(self.name, n)
        return Fun( lambda x: fn(self.function, n, x), name )

    def __call__(self, g):
        """Return the function fog if g is a function Fun,
else return f(g), f is the current function."""
        if type(g) == Fun:
            name = "(%s o %s)" %(self.name, g.name)
            return Fun( lambda x : self(g(x)), name )
        else:
            return self.function(g)

Id = Fun(lambda x : x, "Id")

if __name__ == "__main__" :
    f = Fun(lambda x : x**2, ".**2")










    
