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
            P = "X + " + P
        elif c:
            P = "{}X + ".format(c) + P
        #To have 'aX**k'
        for k in range(2, n+1):
            c = self[k]
            #Having 'X' and not '1X'
            if c == 1:
                P = "X**{} + ".format(k) + P
            elif c:
                P = "{}X**{} + ".format(c, k) + P
        return P

    def __getitem__(self, n):
        """Return the coefficient of X**n. Return 0 if n < 0."""
        if n <= self.deg and n >= 0:
            return self.coef[n]
        else:
            return 0

    def __eq__(self, Q):
        """If Q is a Poly object, return True if their coef are equal, else it returns False.
Return False if Q is something else."""
        if type(Q) == Poly:
            return (self.coef == Q.coef)
        else:
            return False

    #===Operations===
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
        """n is a natural number. Return P**n is the current polynomial."""
        if n:
            S = Poly([1])
            for k in range(n):
                S = S*self
            return S
        else:
            return Poly([1])

    def __call__(self, Q):
        """Q is a Poly, a real or a complex. Return PoQ, P is the current polynomial."""
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
        #Calculate P'
        S = []
        for k in range(self.deg):
            S.append( self[k+1]*(k+1) )
        #Recursive function
        #If n == 0 (or less)
        if n-1 < 0:
            return self
        #If n > 1, calculate P"
        elif n-1:
            return Poly(S).deriv(n-1)
        #If n == 0, return P'
        else:
            return Poly(S)
        
    def unit(self):
        """Return the polynomial X**P.deg, P is the current polynomial."""
        return Poly( [0]*self.deg + [1] )

def pgcd(P, Q):
    """P, Q are Poly object.
Return the PGCD of the polynomial P and Q, using the Euclide algorithm."""
    
    #If (P, Q) == (0, 0), return PGCD(0, 0) = 0
    if (P, Q) == ( Poly(), Poly() ):
        return Poly()
    R = P
    S = Q
    while S.deg >= 0:
        T = R % S
        R = S
        S = T
    return R.unit()

def bezout(P, Q):
    """P, Q are Poly object, with (P, Q) != (0, 0)
Return ( (U,V), R) using the Euclide algorithm, where (U, V) is a pair of Bézout and R is a PGCD."""
    
    #R0 = U0*P + V0*Q
    R0 = P
    U0 = Poly([1])
    V0 = Poly()
    #R1 = U1*P + V1*Q
    R1 = Q
    U1 = Poly()
    V1 = Poly([1])
    while R1.deg >= 0:
        (q, R2) = R0 / R1
        U2 = U0 - q*U1
        V2 = V0 - q*V1
        R0, U0, V0 = R1, U1, V1
        R1, U1, V1 = R2, U2, V2
    return ( (U0, V0), R0)

#For testing
#P = Poly( [42, 1, 1] )
#from numpy import poly1d
#np = poly1d( [1, 1, 42] )
