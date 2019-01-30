#!/usr/bin/env python
#-*- coding: utf-8 -*-

def simplest(coefficients):
    """Delete all the 0 in the end of the list coefficients."""
    #If the list coefficients is not empty
    while coefficients and coefficients[-1] == 0: 
        coefficients.pop(-1)
    return coefficients

class Poly:

    def __init__(self, coef=[]):
        """c is a list of the coefficients of the polynomial, starting with the lowest.
Create a Poly class (By default, the polynomial 0).
Exemple: [42,0,1] -> 42 + X**2"""
        self.coef = simplest(coef)
        #Coefficients (-1 = -inf)
        self.deg = len(self.coef)-1

    def __repr__(self):
        """Print the polynomial as 'aX**n'format."""
        n = self.deg
        P = str(self[0])
        #To have 'aX + b'
        c = self[1]
        #Having 'X' and not '1X'
        if c == 1:
            P = "X" + " + " + P
        elif c:
            P = str(c) + "X" + " + " + P
        #To have 'aX**k'
        for k in range(2, n+1):
            c = self[k]
            #Having 'X' and not '1X'
            if c == 1:
                P = "X**" + str(k) + " + " + P
            elif c:
                P = str(c) + "X**" + str(k) + " + " + P
        return P

    def __getitem__(self, n):
        """Return the coefficient of X**n. Return 0 if n < 0."""
        if n <= self.deg and n >= 0:
            return self.coef[n]
        else:
            return 0

    def __add__(self, Q):
        """Q is a Poly. Return P+Q, P is the current Polynomial."""
        S = []
        n = max([self.deg, Q.deg])
        for k in range(n+1):
            S.append(self[k] + Q[k])
        return Poly(S)

    def __sub__(self, Q):
        """Q is a Poly. Return P-Q, P is the current Polynomial."""
        S = []
        n = max([self.deg, Q.deg])
        for k in range(n+1):
            S.append(self[k] - Q[k])
        return Poly(S)

    def __rmul__(self, K):
        """K is a real or a complex. Return K*P, P is the current Polynomial."""
        S = []
        for i in range(self.deg+1):
            S.append(K*self[i])
        return Poly(S)

    def __mul__(self, Q):
        """Q is a Poly. Return P*Q, P is the current Polynomial."""
        S = []
        for k in range(self.deg + Q.deg +1):
            #c is the coefficient of X**k
            c = 0
            for i in range(k+1):
                c = c + self[i]*Q[k-i]
            S.append(c)
        return Poly(S)

    def __truediv__(self, Q):
        """Q is a Poly. Return (D, R), with P = D*Q + R in the euclidean division, P is the current Polynomial."""
        D = Poly()
        R = self
        while R.deg >= Q.deg:
            c = R[R.deg] / Q[Q.deg]
            deg = R.deg - Q.deg
            S = Poly([0]*deg + [c])
            D = D + S
            R = R - S*Q
        return (D, R)

    def __floordiv__(self, Q):
        """Q is a Poly. Return D, with P = D*Q + R in the euclidean division, P is the current Polynomial."""
        return (self/Q)[0]

    def __mod__(self, Q):
        """Q is a Poly. Return R, with P = D*Q + R in the euclidean division, P is the current Polynomial."""
        return (self/Q)[1]

    def __pow__(self, n):
        """n is a natural number. Return P**k is the current polynomial."""
        if n:
            S = Poly([1])
            for k in range(n):
                S = S*self
            return S
        else:
            return Poly([1])

    def __call__(self, Q):
        """Q is a Polyn, a real or a complex. Return PoQ, P is the current polynomial."""
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

    def deriv(self, n=1):
        """Return the n-derivative of P (by default, P'), P is the current Polynomial."""
        S = []
        for k in range(self.deg):
            S.append( self[k+1]*(k+1) )
        #Recursive function
        if n-1:
            return Poly(S).deriv(n-1)
        else:
            return Poly(S)

#For testing
P = Poly( [42, 1, 1] )
from numpy import poly1d
np = poly1d( [1,1,42] )
