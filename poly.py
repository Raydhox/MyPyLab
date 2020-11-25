#!/usr/bin/env python
#-*- coding: utf-8 -*-

###Some function use numpy; if np is True, everything is fine,
###else, return an error for functions that require numpy.poly1d
##try:
##    from numpy import poly1d
##    np = True
##except:
##    np = False

def simplest(coefficients):
    """Delete all 0 in the end of the list coefficients."""
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

    def adaptability(fun):
        def have_polynomial(self, z):
            """Convert numbers to polynomial if necessary."""
            if type(z) in [int, float, complex]:
                return fun(self, Poly([z]))
            else:
                return fun(self, z)
        return have_polynomial

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
        return (type(Q) == Poly) and (self.coef == Q.coef)

    #===Operations===
    @adaptability
    def __add__(self, Q):
        """Q is a Poly. Return P+Q, P is the current polynomial."""
        S = []
        n = max([self.deg, Q.deg])
        for k in range(n+1):
            S.append(self[k] + Q[k])
        return Poly(S)

    @adaptability
    def __sub__(self, Q):
        """Q is a Poly. Return P-Q, P is the current polynomial."""
        S = []
        n = max([self.deg, Q.deg])
        for k in range(n+1):
            S.append(self[k] - Q[k])
        return Poly(S)

    def __rmul__(self, k):
        """K is a real or a complex. Return K*P, P is the current polynomial."""
        S = []
        for i in range(self.deg+1):
            S.append(k*self[i])
        return Poly(S)

    @adaptability
    def __mul__(self, Q):
        """Q is a Poly. Return P*Q, P is the current polynomial."""
        if type(Q) == Poly:
            S = []
            for k in range(self.deg + Q.deg +1):
                #c is the coefficient of X**k
                c = 0
                for i in range(k+1):
                    c = c + self[i]*Q[k-i]
                S.append(c)
            return Poly(S)
        else:
            return Q.__rmul__(self)

    def __truediv__(self, Q):
        """Q is a Poly. Return (D, R), with P = D*Q + R in the euclidean division, P is the current polynomial."""
        if type(Q) in [int, float, complex]:
            return self.__rmul__(1/Q)
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
        """Q is a Poly. Return D, with P = D*Q + R in the euclidean division, P is the current polynomial."""
        return (self/Q)[0]

    def __mod__(self, Q):
        """Q is a Poly. Return R, with P = D*Q + R in the euclidean division, P is the current polynomial."""
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
        """Q is a Poly, a real or a complex. P(Q) return the composition PoQ, P is the current polynomial."""
        #Q is a real or a complex
        if type(Q) in [int, float, complex]:
            #Horner algorithm
            S = self[self.deg]
            for k in range(self.deg):   #/!\ What the hell am I playing with self.deg ???????????????????????!!!!
                S = S*Q + self[self.deg-k-1] 
            return S 
        #Q is a Poly
        if type(Q) == Poly:
            if Q.deg == -1:
                return Poly([0])
            else:
                S = Poly()
                for k in range( self.deg*Q.deg ):
                    S = S + self[k]*(Q**k)
                return S
        #Q is something else that understand (+, *, **)...
        #S = 0 of type(Q)
        S = Q - Q
        for k in range(self.deg+1):
            S = S + self[k] * Q**k
        return S

    def deriv(self, n=1):
        """Return the n-derivative of P (by default, P'), P is the current polynomial."""
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
        #If n == 1, return P'
        else:
            return Poly(S)
        
    def unit(self):
        """Return the polynomial X**P.deg, P is the current polynomial."""
        if self != Poly():
            return 1/self[self.deg]*self
        else:
            return self

    def pgcd(self, Q):
        """Q is a Poly object, P is the current polynomial
    Return the PGCD of the polynomial P and Q, using the Euclide algorithm."""
        
        #If (P, Q) == (0, 0), return PGCD(0, 0) = 0
        if (self, Q) == ( Poly(), Poly() ):
            return Poly()
        R = self
        S = Q
        while S.deg >= 0:
            T = R % S
            R = S
            S = T
        return R.unit()

    def bezout(self, Q):
        """Q is a Poly object, is the current polynomial, with (P, Q) != (0, 0).
    Return ( (U,V), R) using the Euclide algorithm, where (U, V) is a pair of Bézout and R is a PGCD."""
        
        #R0 = U0*P + V0*Q
        R0 = self
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

#=====================================================================================================================================================#
class Fraction:

    def __init__(self, A, B=Poly([1]) ):
        """Return an algbraic fraction. B must be a Poly.
If A is a Fraction, return A.
If A is a Polynomial, return the algebraic fraction A/B."""
        if type(A) == Fraction:
            self.num, self.den, self.deg = A.num, A.den, A.deg
        else:
            self.num = A
            self.den = B
            self.deg = A.deg - B.deg

    def init(self):
        """Return a proper rational fraction and create self.mod."""
        #[FR]: floor est la partie entière
        self.floor, mod = self.num / self.den
        self.mod = Fraction(mod, self.den)
        return self
            
    def __repr__(self):
        """Print the algebraic fraction as num/den."""
        n = max( len(str(self.num)), len(str(self.den)) )
        return "{}\n{}\n{}".format( str(self.num), "-"*n, str(self.den) )

    def __eq__(self, R):
        """If R is a Fraction object, return True if their euclidean division of numerator / denominator are equal,
else it returns False.
Return False if R is not a Fraction object."""
        return (self.num * R.den == R.num * self.den)

    #===Operations===
    def __add__(self, R):
        """R is a Fraction or a Poly. Return S+R, S is the current Fraction."""
        R = Fraction(R)
        A = self.num*R.den + R.num*self.den
        B = self.den*R.den
        return Fraction(A, B)

    def __sub__(self, R):
        """R is a Fraction or a Poly. Return S-R, S is the current Fraction."""
        R = Fraction(R)
        A = self.num*R.den - R.num*self.den
        B = self.den*R.den
        return Fraction(A, B)

    def __rmul__(self, k):
        """k is a real or a complex. Return k*S, S is the current Fraction."""
        return Fraction( k*self.num, self.den)

    def __mul__(self, R):
        """R is a Fraction or a Poly. Return S*R, S is the current Fraction."""
        R = Fraction(R)
        return Fraction( self.num*R.num, self.den*R.den)

    def __truediv__(self, R):
        """R is a Fraction or a Poly. Return S*1/R, S is the current Fraction."""
        R = Fraction(R)
        return Fraction( self.num*R.den, self.den*R.num)

    def __pow__(self, n):
        """n is a natural number. Return S**n, S is the current Fraction."""
        if n > 0:
            R = Fraction( Poly([1]) )
            for k in range(n):
                R = R*self
            return R
        elif n < 0:
            return Fraction(self.den, self.num).__pow__(-n)
        else:
            return Fraction( Poly([1]) )

    def __call__(self, X):
        """X is a real or a complex. Return the composition SoX, S is the current Fraction."""
        return self.num(X) / self.den(X)

    def deriv(self, n=1):
        """Return the n-derivative of S (by default, S'), S is the current Fraction."""
        #Calculate R'
        A = self.num.deriv()*self.den - self.num*self.den.deriv()
        B = self.den**2
        #Recursive function
        #If n == 0 (or less)
        if n-1 < 0:
            return self
        #If n > 1, calculate R"
        elif n-1:
            return Fraction(A, B).deriv(n-1)
        #If n == 1, return R'
        else:
            return Fraction(A, B)

##    def part(self):
##        """Return the partial fraction decomposition. Need numpy.
##Doesn't work for most case."""
##        if np is False:
##            raise ModuleNotFoundError("Need numpy.poly1d.")
##        #Convert to a numpy.poly1d object
##        self.den.coef.reverse()
##        roots = poly1d(self.den.coef).roots
##        self.den.coef.reverse()
##        #Lists of constants
##        C = []
##        self.init()
##        for z in roots:
##            #Convert roots from numpy.complex to complex
##            z = complex(z)
##            #S = self.mod.den / (X-z)
##            S = (self.mod.den // Poly([-z, 1]))
##            C.append( self.mod.num(z) / S(z) )
##        return (self.floor, C)


            
#For testing
if __name__ == "__main__":
    P = Poly( [42, 1, 1] )
    R = Fraction( P, Poly([4,2]) )
    #if np:
    #    np = poly1d( [1, 1, 42] )

    P = Poly( [7,6,-2] )
    Q = Poly( [4,0,5,0,1] )
    R = Fraction(P, Q)
    #print( R.part() )


















