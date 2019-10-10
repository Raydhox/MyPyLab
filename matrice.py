"""Module permettant d'utiliser les matrices.
Par flemme, l'utilisateur doit définir les matrices avant de pouvoir
les utiliser (lors des opérations notamment).
Le programme n'est pas optimisée (déterminant/inverse)
et de nombreux erreurs sont possibles (Matrice non carré qu'on essaie d'inverser,
Matrice définie à partie d'une liste ne respectant les dimensions...).

Enfin, le meilleur conseil que je puisse donner: Numpy, Scipy >> matrice.py"""

import copy

class Mat:
    
    def __init__(self, option=[[1,2],[3,4]]):
        """option peut-être:
        Une liste de liste(s) définissant une matrice.
        Un tuple qui donnera une matrice colonne.
        Un nombre n, qui donnera la matrice identité n.
        La matrice est stockée dans la variable value."""
        #La matrice vaut la liste de dimension colonne*ligne."""
        if type(option) == list:
            self.value = option
            self.dim = ( len(option[0]), len(option) )
        #Matrice colonne
        elif type(option) == tuple:
            self.value = []
            self.dim = ( 1, len(option) )
            for k in range(len(option)):
                self.value.append( [option[k]] )
        #Matrice carré d'ordre 'option'
        elif type(option) == int:
            self.value = []
            self.dim = ( option, option )
            for k in range(option):
                self.value.append( [0]*k +[1] + [0]*(option-k-1) )
        else:
            print("Option non valide; la matrice [[0]] sera définie par défaut.")
            self.value = [[0]]
            
    def __repr__(self):
        """Permet d'afficher l'objet matrice comme une matrice (listes surperposées)."""
        afficher = ""
        for k in range(len(self.value)):
            afficher += str(self.value[k]) + "\n"
        return afficher

    def __getitem__(self, index):
        """Récupère une valeur précise [i][j] de la Matrice."""
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
        if (type(facteur) == int) or (type(facteur) == float):
            for ligne in range(self.dim[0]):
                produit.append([])
                for col in range(self.dim[1]):
                    produit[ligne].append( facteur*self.value[ligne][col] )
            return Mat(produit)
        #Les erreurs
        else:
            print("Erreur: Ne multiplier des matrices qu'avec des matrices ou des nombres entiers.")

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

    def inv(self):
        #A = copy.deepcopy(self.value)
        #Matrice augmentée
        A = []
        identite = Mat(len(self.value))
        for ligne in range(len(self.value)):
            A.append( copy.deepcopy(self.value[ligne]) + identite.value[ligne] )
        #On veut diagonalisé la matrice
        for k in range( len(self.value) ):
            #On échelonne la matrice
            for i in range( len(self.value)-1 ):
                #Transvection
                coeff_a = A[k][k]
                coeff_b = A[k-1-i][k]
                for j in range( 2*len(self.value) ):
                    A[k-1-i][j] = coeff_a*A[k-1-i][j] - coeff_b*A[k][j]
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
            print("Matrice non inversible.")
            
##    def inv2(self):
##        """Retourne l'inverse de la matrice, tout comme Mat**-1.
##        Utilise la méthode du pivot de Gauss-Jordan: https://fr.wikipedia.org/wiki/%C3%89limination_de_Gauss-Jordan#Calcul_de_l'inverse_d'une_matrice_carr%C3%A9e"""
##        #Matrice augmentée
##        A = []
##        identite = Mat(len(self.value))
##        for ligne in range(len(self.value)):
##            A.append( copy.deepcopy(self.value[ligne]) + identite.value[ligne] )
##        #Gauss-Jordan
##        r = -1
##        #
##        for j in range(self.dim[1]):
##            print(Mat(A), "\n")
##            #Les colonnes deviennent des lignes et les lignes, des colonnes.
##            B = copy.deepcopy(self.value)
##            for col in range(self.dim[1]):
##                B.append([])
##                for ligne in range(self.dim[0]):
##                    B[col].append( A[ligne][col] )
##            #k = max(|A[i,j]|, r+1 ≤ i ≤ n)
##            m = max( B[r+1][j:] )
##            k = 0
##            for ligne in range(self.dim[0]):
##                if B[r+1][ligne] == m:
##                    k = ligne
##            #Combinaisons linéaires
##            if A[k][j] != 0:#self.value[k][j] != 0:
##                r += 1
##                #Diviser la ligne k par A[k,j]
##                Akj = A[k][j]
##                for col in range(2*self.dim[1]):
##                    A[k][col] /= Akj
##                #Échanger les lignes k et r
##                if A[k] != A[r]:
##                    apermuter = A[k]
##                    A[k] = A[r]
##                    A[r] = apermuter
##                #On simplifie les autres lignes
##                for i in range(self.dim[0]):
##                    if i != r:
##                        #Soustraire à la ligne i la ligne r multipliée par A[i,j]
##                        Aij = A[i][j]
##                        for col in range(2*self.dim[1]):
##                            A[i][col] -= A[r][col]*Aij
##        #Matrice inverse
##        M = []
##        for ligne in range(len(self.value)):
##            M.append( A[ligne][len(self.value):] )
##        #Arrondie
##        for ligne in range(len(self.value)):
##            for col in range(len(self.value)):
##                M[ligne][col] = round(M[ligne][col], 5)
##        if self.det():
##            return Mat(M)
##        else:
##            print("Matrice non inversible.")
            
    
    def det(self):
        """Fonction calculant et retournant le déterminant. Calcul aussi la matrice inverse.
        Utilise la méthode du pivot de Gauss-Jordan: https://fr.wikipedia.org/wiki/%C3%89limination_de_Gauss-Jordan"""
        #Copie de la matrice + determinant
        A = copy.deepcopy(self.value)
        p = 0
        pivot = 0
        try:
            #Gauss-Jordan
            r = -1
            #
            for j in range(self.dim[1]):
                #Les colonnes deviennent des lignes et les lignes, des colonnes.
                B = []
                for col in range(self.dim[1]):
                    B.append([])
                    for ligne in range(self.dim[0]):
                        B[col].append( abs(A[ligne][col]) )
                #k = max(|A[i,j]|, r+1 ≤ i ≤ n)
                m = max( B[r+1][j:] )
                k = 0
                for ligne in range(self.dim[0]):
                    if B[r+1][ligne] == m:
                        k = ligne
                #Combinaisons linéaires
                if self.value[k][j] != 0:
                    r += 1
                    #Diviser la ligne k par A[k,j]
                    Akj = A[k][j]
                    #Produit des pivots
                    if pivot:
                        pivot *= Akj
                    else:
                        pivot = Akj
                    for col in range(self.dim[1]):
                        A[k][col] /= Akj
                    #Échanger les lignes k et r
                    if A[k] != A[r]:
                        apermuter = A[k]
                        A[k] = A[r]
                        A[r] = apermuter
                        p += 1
                    #On simplifie les autres lignes
                    for i in range(self.dim[0]):
                        if i != r:
                            #Soustraire à la ligne i la ligne r multipliée par A[i,j]
                            Aij = A[i][j]
                            for col in range(self.dim[1]):
                                A[i][col] -= A[r][col]*Aij
            #Déterminant
            return pivot*(-1)**p
        #Déterminant = 0
        except:
            return 0
		
#=====Pour tester=====
A = Mat()# [[1,2],[3,4]]
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










