#!/usr/bin/env python
#-*- coding: utf-8 -*-

def simplest(coefficients):
    while coefficients[-1] == 0 and len(coefficients) > 1: 
        coefficients.pop(-1)
    return coefficients

class Poly:

    def __init__(self, coefficients):
        """coeff is a list of the coefficients, starting with the lowest.
Create a Polynome class. Exemple: [42,0,1] -> 42 + X**2"""
        self.coef = simplest(coefficients)
        #Coefficients (-1 = -inf)
        if self.coef == [0]:
            self.deg = -1
        else:
            self.deg = len(self.coef)

    def __repr__(self):
        """Print a Polynome as 'aX**n'."""
        n = self.deg
        P = str(self.coef[0])
        if n >= 1:
            P = P + " + " + str(self.coef[1]) + "X"
        if n >= 2:
            for k in range(n-1, 2, -1):
                P = P + " + " + str(self.coef[k]) + "X**" + str(k)
        return P

    def __getitem__(self, index):
        """Return index """
        return self.coef[index]

    def __add__(self, Q):
        """Add P+Q, P is the current Polynome."""
        S = []
        n = min([self.deg, Q.deg])
        for k in range(n):
            S.append(self.coef[k] + Q.coef[k])
        return Polynome(S + self.coef[n:] + Q[n:])
    
P = Polynome( [42, 1, 1] )
