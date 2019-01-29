#!/usr/bin/env python
#-*- coding: utf-8 -*-

def simplest(coefficients):
    while coefficients[-1] == 0 and len(coefficients) > 1: 
        coefficients.pop(-1)
    return coefficients

class Poly:

    def __init__(self, c=[0]):
        """c is a list of the coefficients, starting with the lowest.
Create a Polynome class. Exemple: [42,0,1] -> 42 + X**2"""
        self.coef = simplest(c)
        #Coefficients (-1 = -inf)
        if self.coef == [0]:
            self.deg = -1
        else:
            self.deg = len(self.coef)-1

    def __repr__(self):
        """Print the polynomial as 'aX**n'format."""
        n = self.deg
        P = str(self.coef[0])
        #To have 'aX + b'
        if n >= 1:
            c = self.coef[1]
            if c == 1:
                P = "X" + " + " + P
            else:
                P = str(c) + "X" + " + " + P
        #To have 'aX**k'
        if n >= 2:
            for k in range(2, n+1):
                c = self.coef[k]
                if c == 0:
                    pass
                elif c == 1:
                    P = "X**" + str(k) + " + " + P
                else:
                    P = str(c) + "X**" + str(k) + " + " + P
        return P

    def __getitem__(self, n):
        """Return the coefficient of X**n."""
        try:
            return self.coef[n]
        except IndexError:
            return 0

    def __add__(self, Q):
        """Q is a Polynomial. Return P+Q, P is the current Polynomial."""
        S = []
        n = max([self.deg, Q.deg])
        for k in range(n+1):
            S.append(self[k] + Q[k])
        return Poly(S)

    def __sub__(self, Q):
        """Q is a Polynomial. Return P-Q, P is the current Polynomial."""
        S = []
        n = max([self.deg, Q.deg])
        for k in range(n+1):
            S.append(self[k] - Q[k])
        return Poly(S)

    def __rmul__(self, K):
        """K is a real or a complex. Return K*P, P is the current Polynomial."""
        S = []
        for k in range(self.deg+1):
            S.append(K*self[k])
        return Poly(S)

    def __mul__(self, Q):
        """Q is a Polynomial. Return P*Q, P is the current Polynomial."""
        S = []
        for k in range(self.deg + Q.deg +1):
            #c is the coefficient of X**k
            c = 0
            for i in range(k+1):
                c = c + self[i]*Q[k-i]
            S.append(c)
        return Poly(S)

    def __truediv__(self, Q):
        """Q is a Polynomial. Return (D, R), with P = D*Q + R (deg R < deg Q), P is the current Polynomial."""
        D = Poly()
        R = self
        while R.deg >= Q.deg:
            c = R[-1] / Q[-1]
            deg = R.deg - Q.deg
            S = Poly([0]*deg + [c])
            D = D + S
            R = R - S*Q
        return (D, R)

    def __pow__(self, n):
        """n is a natural number. Return P**k is the current Polynomial."""
        if n:
            S = Poly([1])
            for k in range(n):
                S = S*self
            return S
        else:
            return Poly([1])

    def __call__(self, Q):
        """Q is a Polynomial, or a real (or a complex). Return PoQ, P is the current Polynomial."""
        #Q is a real or a complex
        if type(Q) in [int, float, complex]:
            S = 0
            for k in range(self.deg +1):
                S = S + self[k]*Q**k
            return S
        #Q is a Poly
        if Q.deg == -1:
            return Poly([0])
        else:
            S = Poly()
            for k in range( self.deg*Q.deg ):
                S = S + self[k]*(Q**k)
            return S

#For testing
P = Poly( [42, 1, 1] )
from numpy import poly1d
np = poly1d( [1,1,42] )
