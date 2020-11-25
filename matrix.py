#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""Module permettant d'utiliser les matrices.
Par flemme, l'utilisateur doit définir les matrices avant de pouvoir
les utiliser (lors des opérations notamment).
Le programme n'est pas optimisée (déterminant/inverse)
et de nombreux erreurs sont possibles (Matrice non carré qu'on essaie d'inverser,
Matrice définie à partie d'une liste ne respectant les dimensions...).

Enfin, le meilleur conseil que je puisse donner: Numpy >> all"""

import copy
from poly import Poly

class Mat:

    def __init__(self, option):
        """option peut-être:
        Une liste de liste(s) définissant une matrice.
        Un tuple qui donnera une matrice colonne.
        Un nombre n, qui donnera la matrice identité n.
        La matrice est stockée dans la variable value."""
        #La matrice vaut la liste de dimension ligne*colonne."""
        if type(option) == list:
            self.value = option
            self.dim = ( len(option), len(option[0]) )
        #Tuple = Matrice colonne
        elif type(option) == tuple:
            self.value = []
            self.dim = ( len(option), 1 )
            for k in range(len(option)):
                self.value.append( [option[k]] )
        #Matrice identité d'ordre 'option'
        elif type(option) == int:
            self.value = []
            self.dim = ( option, option )
            for i in range(option):
                self.value.append( [ int((i == j)) for j in range(option) ] )
        else:
            self.value = [[0]]
                
    def __repr__(self):
        """Permet d'afficher l'objet matrice comme une matrice (listes surperposées)."""
        afficher = ""
        for k in range(len(self.value)):
            afficher += str(self.value[k]) + "\n"
        return afficher
    
    def __getitem__(self, index):
        """Return the line(s) index, or the column(s) index if index is a list."""
        if type(index) == list :
            extract = []
            for col in index:
                extract.append( [ self.value[k][col] for k in range(self.dim[0]) ] )
            return extract
        return self.value[index]


    def __add__(self, terme):
        somme = []
        if (type(terme) == Mat) and (self.dim == terme.dim):
            for ligne in range(self.dim[0]):
                somme.append([])
                for col in range(self.dim[1]):
                    somme[ligne].append(self.value[ligne][col] + terme.value[ligne][col])
            return Mat(somme)

    def __sub__(self, terme):
        #Additione les termes des deux matrices un à un.
        somme = []
        if (type(terme) == Mat) and (self.dim == terme.dim):
            for ligne in range(self.dim[0]):
                somme.append([])
                for col in range(self.dim[1]):
                    somme[ligne].append(self.value[ligne][col] - terme.value[ligne][col])
            return Mat(somme)

    def __mul__(self, facteur):
        #Multiplie les termes des deux matrices un à un.
        produit = []
        if (type(facteur) == Mat) and (self.dim[0] == facteur.dim[1]):
            for ligne in range(self.dim[1]):
                produit.append([])
                for col in range(facteur.dim[0]):
                    somme = 0
                    for k in range(self.dim[0]):
                        somme += self.value[ligne][k]*facteur.value[k][col]
                    produit[ligne].append(somme)
            return Mat(produit)
        #Les erreurs
        elif (type(facteur) == Mat):
            print("Erreur de dimensions.")
        else:
            print("Erreur: Ne multiplier des matrices qu'avec des matrices; pour les réels, mettez les à gauche.")
                                                
    def __rmul__(self, facteur):
        #Multiplie chaque terme de la matrice un à un par la constante.
        produit = []
        #if type(facteur) in [int, float, complex]:
        for ligne in range(self.dim[0]):
            produit.append([])
            for col in range(self.dim[1]):
                produit[ligne].append( self.value[ligne][col]*facteur )
        return Mat(produit)

    def __pow__(self, exposant):
        #Entier naturel non nul => Répétition de multiplication.
        if (type(exposant) == int) and (exposant > 0):
            puissance = Mat(self.value)
            for facteur in range(exposant-1):
                puissance *= Mat(self.value)
            return puissance
        #Renvoie la matrice identité si matrice carré.
        elif (exposant == 0) and (self.dim[0] == self.dim[1]):
            return Mat(self.dim[0])
        #Inverse
        elif (exposant == -1) and (self.dim[0] == self.dim[1]):
            return self.inv()
        #Les erreurs
        elif (type(exposant) != int) or (exposant < -1):
            print("Erreur: L'exposant doit être un entier compris entre [ -1; +\infty [ ")
        else:
            print("Matrice non inversible.")

    def transpose(self):
        """Retourne la transposé de la matrice."""
        T = []
        for col in range(self.dim[1]):
            T.append([])
            for line in range(self.dim[0]):
                T[col].append( self.value[line][col] )
        return Mat(T)

    def dagger(self):
        """Retourne l'adjoint de la matrice."""
        A = self.transpose()
        for i in range(A.dim[0]):
            for j in range(A.dim[1]):
                A[i][j] = A[i][j].conjugate()
        return A

    def adjoint(self):
        return self.dagger()


    def inv(self):
        assert self.dim[0] == self.dim[1]
        #A = copy.deepcopy(self.value)
        #Matrice augmentée
        A = []
        identite = Mat(len(self.value))
        for ligne in range(len(self.value)):
            A.append( copy.deepcopy(self.value[ligne]) + identite.value[ligne] )
        #On veut diagonaliser la matrice;
        #On parcourt ainsi les colonnes de la matrice.
        for k in range( len(self.value) ):
            
            #===Recherche du pivot===
            #Recherche de l'indice du pivot, (le maximum absolu):
            pivoti, pivot = k, abs(A[k][k])
            for r in range( k, len(self.value) ):
                if abs(A[r][k]) > pivot:
                    pivoti = r
                    pivot = abs(A[r][k])
            #Échange de lignes:
            A[k], A[pivoti] = A[pivoti], A[k]

            #===On inverse la matrice===
            pivot = A[k][k]
            #On parcourt les lignes ainsi: k-1, k-2, ... 1, n, n-1...
            for i in range( len(self.value)-1 ):
                #Combinaison linéaire (en fait, il s'agirait d'une transvection
                #en divisant par le pivot, mais le pivot peut être nul).
                coeff = A[k-1-i][k]
                for j in range( 2*len(self.value) ):
                    A[k-1-i][j] = pivot*A[k-1-i][j] - coeff*A[k][j]
        try:
            #Identité (les -1 deviennent des 1)
            for i in range( len(self.value) ):
                coeff = A[i][i]
                for j in range( 2*len(self.value) ):
                    A[i][j] /= coeff
            #Matrice inverse
            M = []
            for ligne in range(len(self.value)):
                M.append( A[ligne][len(self.value):] )
            return Mat(M)
        except ZeroDivisionError:
            print("Non inversible")
        


    def cofacteur(self, i, j):
        assert self.dim[0] == self.dim[1]
        """Retourne la comatrice d'indice i, j."""
        C = []
        for line in range(self.dim[0]):
            if line != i:
                C.append([])
                for col in range(self.dim[1]):
                    if col != j:
                        C[-1].append(self[line][col])
        return (-1)**(i+j) * ( Mat(C).det() )

   
    def det(self):
        assert self.dim[0] == self.dim[1]
        """Fonction calculant et retournant le déterminant de manière récursive (pour pouvoir calculer le poca)."""
        if self.dim[0] == 0:
            return 0
        elif self.dim[0] == 1:
            return self[0][0]
        elif self.dim[0] == 2:
            return self[0][0]*self[1][1] - self[1][0]*self[0][1]
        #else:
        D = self[0][0] * self.cofacteur(0, 0)
        for k in range(1, self.dim[0]):
            D = D + self[k][0] * self.cofacteur(k, 0)
        return D

    def poca(self):
        assert self.dim[0] == self.dim[1]
        X = Poly([0, 1])
        #X*Id - M
        ksi = X*Mat(self.dim[0]) - self
        return ksi.det()

    def exp(self, n=10):
        """Retourne une approximation de l'exponentielle matricielle,
n étant le rang de la somme partielle, selon la définition en série entière."""
        assert self.dim[0] == self.dim[1]
        E = 0*Mat(self.dim[0])
        kappa = 1
        for k in range(n):
            if k:
                kappa *= k
            E = E + (1/ kappa) * self**k
        return E

def Zeros(m, n=None):
    """Return the zeros matrix."""

    if n == None :
        n = m
    value = []
    for k in range(m):
        value.append( [0]*n )
    return Mat(value)


#=====Pour tester=====
if __name__ == "__main__":         
    A = Mat( [[1,2],[3,4]] )
    Z = Mat( [[0,0],[0,0],[0,0]] )
    #Ligne
    L = Mat( [[1, 2]] )
    #Colonne
    C = Mat( (1, 2) )
    #Identité
    I = Mat(2)
    #Wikipédia
    #B = Mat( [[2,-1,0],[-1,2,-1],[0,-1,2]] )
    #D = Mat( [[2,-1,0],[0,-1,2],[-1,2,-1]] )

    #Test pour un DM de maths en prépa...
    P = Mat([[1,-1,2],[-1,0,3],[1,-1,1]])
    #Q = Mat([[3,-1,-3],[4,-1,-5],[1,0,-1]])

    M = Mat([[0, 1], [-1, 0]])
    N = -1*M









