import numpy as np
import random

# -2 = Trouve/joué
# -1 = Bombe
# 0 = Vide

# Il y a deux tableau
# Plateau = qui va avec des nombres indiquées au dessus calculer les nombres du jeu et indique les emplacements pas des nombres
# Affiche = qui va en fonction de plateau afficher :
#   X si -2
#   B si -1
#   entier > 0 affiche l'entier
#   et si il y a des nombres autour des X ils s'afficheront également


class Demineur:
    # ------------------------ Constructeur ------------------------ #
    def __init__(self, taille : int, nbBombe : int):
        self.__taille : int = taille
        self.__nbBombe : int = nbBombe
        self.__plateau : np.ndarray = np.full([self.__taille,self.__taille], 0, dtype=object)
        self.__affichage : np.ndarray = np.empty([self.__taille,self.__taille], dtype=object)
        self.__perdu : int = 0
        self.__gagne : int = 0
        self.__nbAffichage : int = 0
        
        self.initialise()
        self.remplirBombe()
        self.compteBombe()
          
    # ------------------------ Méthodes ------------------------ #
    
    # initialise le tableau affichage avec des chaines de caracètres vides et initialise le tableau plateau avec des 0
    def initialise(self):
        for i in range(len(self.__affichage)):
            for y in range(len(self.__affichage)):
                    self.__affichage[i][y] = " "
        self.__plateau : np.ndarray = np.full([self.__taille,self.__taille], 0, dtype=object)

    # remplis le tableau plateau de bombe de façon aléatoire
    def remplirBombe(self) -> None:
        max : int = 0
        for i in range(self.__taille):
            x : int = random.randint(0, self.__taille-1)
            y : int = random.randint(0, self.__taille-1)
            if max < self.__nbBombe:
                self.__plateau[x][y] = -1
                max += 1
    # compte les cases si elles sont entourées de bombe si oui cela indique combien à la case dans le tableau plateau
    def compteBombe(self) -> None:
        for i in range(self.__taille):
            for col in range(self.__taille):
                nb : int = 0
                if (self.__plateau[i][col] == 0):
                    if ((col < self.__taille-1)):
                        if ((self.__plateau[i][col+1] == -1)):
                            nb+= 1
                    if ((col > 0)):
                        if ((self.__plateau[i][col-1] == -1)):
                            nb+= 1
                    if ((i < self.__taille-1)):
                        if ((self.__plateau[i+1][col] == -1)):
                            nb+= 1
                    if ((i > 0)):
                        if ((self.__plateau[i-1][col] == -1)):
                            nb+= 1
                    if (i < self.__taille-1 and col < self.__taille-1):
                        if ((self.__plateau[i+1][col+1] == -1)):
                            nb+= 1
                    if (i > 0 and col > 0):
                        if ((self.__plateau[i-1][col-1] == -1)):
                            nb+= 1
                    if (i > 0 and col < self.__taille-1):
                        if ((self.__plateau[i-1][col+1] == -1)):
                            nb+= 1
                    if (i < self.__taille-1 and col > 0):
                        if ((self.__plateau[i+1][col-1] == -1)):
                            nb+= 1
                               
                    self.__plateau[i][col] = int(nb)

    # permet de vérifier si toutes les cases hors des bombes on était découverte , si oui alors on retourne True pour avoir gagner sinon False
    def verifGagne(self) -> bool:
        nb = 0
        for ligne in range(self.__taille):
            for col in range(self.__taille):
                if self.__plateau[ligne][col] == -2:
                    nb+=1
        if nb != ((self.__taille*self.__taille)-self.__nbBombe):
            return False
        else:
            return True

    # permet de joue à l'endroit séléctionner avec deux entiers en paramètres et de verifier si c'est une bombe ou si la case est vide pour permettre de jouer
    # permet également de compter le nombre de fois perdu et gagné et si la parti est gagner ou perdu
    def joue(self, ligne : int, col : int) -> None:
        self.__nbAffichage = 0
        if (self.__plateau[ligne-1][col-1] == -1):
            self.__affichage[ligne-1][col-1] = "B"
            self.__perdu += 1
            self.__nbAffichage = 1
        else:
            if (self.__plateau[ligne-1][col-1] == 0):
                    self.verifAllVide(ligne-1 , col-1) 
                    self.afficheCompteBombe() 
            if (self.__plateau[ligne-1][col-1] > 0):
                if (self.__affichage[ligne-1][col-1] == " "):   
                    self.__affichage[ligne-1][col-1] = ""+ str(self.__plateau[ligne-1][col-1])+ ""
                    self.__plateau[ligne-1][col-1] = -2  
        if(self.verifGagne() == True):
                self.__gagne += 1
                self.__nbAffichage = 2  
        if (self.__nbAffichage > 0):
            self.showAll()
            
    # permet à la fin d'une partie d'afficher toutes les bombes et donc ici d'afficher au tableau affichage toutes les bombes présentes      
    def showAll(self):
        for i in range(len(self.__affichage)):
            for y in range(len(self.__affichage)):
                if self.__plateau[i][y] == -1 and self.__affichage[i][y] == " ":
                    self.__affichage[i][y] = "B"
                    
    # permet de vérifier quand on joue si a autour de l'emplacement joué il y a des emplacements vide, si c'est vide cela est indiqué comme joué et cela fait comme des sortes de "cratères"
    def verifAllVide(self, lignee : int, coll : int) -> None:
        afaire = []
        afaire.append((lignee, coll))
        while len(afaire) != 0:
            ligne = afaire[0][0]
            col = afaire[0][1]
            if (col < self.__taille-1):
                if ((self.__plateau[ligne][col+1] == 0) and (ligne,col+1) not in afaire):
                    afaire.append((ligne,col+1))
            if ((col > 0)):
                if ((self.__plateau[ligne][col-1] == 0) and (ligne,col-1) not in afaire):
                    afaire.append((ligne,col-1))
            if ((ligne < self.__taille-1)):
                if ((self.__plateau[ligne+1][col] == 0) and (ligne+1,col) not in afaire):
                    afaire.append((ligne+1,col))
            if ((ligne> 0)):
                if ((self.__plateau[ligne-1][col] == 0) and (ligne-1,col) not in afaire):
                    afaire.append((ligne-1,col))
            if (ligne < self.__taille-1 and col < self.__taille-1):
                if ((self.__plateau[ligne+1][col+1] == 0) and (ligne+1,col+1) not in afaire):
                    afaire.append((ligne+1,col+1))
            if (ligne > 0 and col > 0):
                if ((self.__plateau[ligne-1][col-1] == 0) and (ligne-1,col-1) not in afaire):
                    afaire.append((ligne-1,col-1))
            if (ligne > 0 and col < self.__taille-1):
                if ((self.__plateau[ligne-1][col+1] == 0) and (ligne-1,col+1) not in afaire):
                    afaire.append((ligne-1,col+1))
            if (ligne < self.__taille-1 and col > 0):
                if ((self.__plateau[ligne+1][col-1] == 0) and (ligne+1,col-1) not in afaire):
                    afaire.append((ligne+1,col-1))
                    
            for g in afaire:
                l = g[0]
                c = g[1]
                self.__plateau[l][c] = -2
        
            afaire.remove((ligne, col))
            
    # permet d'afficher les endroits joué entourer et entourer des nombres si il y en a (entourer de X sur le tableau affichage)  
    def afficheCompteBombe(self):
        kk = []
        for i in range(len(self.__affichage)):
            for y in range(len(self.__affichage)):
                if self.__plateau[i][y] == -2 and self.__affichage[i][y] == " ":
                    self.__affichage[i][y] = "X"
                    if (i < self.__taille-1 and y < self.__taille-1 and self.__plateau[i+1][y+1] > 0):
                        self.__affichage[i+1][y+1] = ""+ str(self.__plateau[i+1][y+1])+ ""
                        kk.append((i+1, y+1))
                    if ((y < self.__taille-1) and self.__plateau[i][y+1] > 0):
                        self.__affichage[i][y+1] = ""+ str(self.__plateau[i][y+1])+ ""
                        kk.append((i, y+1))
                    if ((y > 0) and self.__plateau[i][y-1] > 0):
                        self.__affichage[i][y-1] = ""+ str(self.__plateau[i][y-1])+ ""
                        kk.append((i, y-1))
                    if ((i < self.__taille-1) and self.__plateau[i+1][y] > 0):
                        self.__affichage[i+1][y] = ""+ str(self.__plateau[i+1][y])+ ""
                        kk.append((i+1, y))
                    if ((i > 0) and self.__plateau[i-1][y] > 0):
                        self.__affichage[i-1][y] = ""+ str(self.__plateau[i-1][y])+ ""
                        kk.append((i-1, y))         
                    if (i > 0 and y > 0 and self.__plateau[i-1][y-1] > 0):
                        self.__affichage[i-1][y-1] = ""+ str(self.__plateau[i-1][y-1])+ ""
                        kk.append((i-1, y-1))
                    if (i > 0 and y < self.__taille-1 and self.__plateau[i-1][y+1] > 0):
                        self.__affichage[i-1][y+1] = ""+ str(self.__plateau[i-1][y+1])+ ""
                        kk.append((i-1, y+1))
                    if (i < self.__taille-1 and y > 0 and self.__plateau[i+1][y-1] > 0):
                        self.__affichage[i+1][y-1] = ""+ str(self.__plateau[i+1][y-1])+ ""
                        kk.append((i+1, y-1))
        for v in kk:
            l = v[0]
            c = v[1]
            self.__plateau[l][c] = -2

    # permet de relancer une nouvelle parti, sois de tout rénitialiser
    def nouvellePartie(self) -> None:
        self.initialise()
        self.remplirBombe()
        self.compteBombe()
        self.__nbAffichage = 0
    
    # permet de récupérer la valeur de l'attribut taille
    def getTaille(self) -> int:
        return self.__taille

    # permet de récupérer ce qu'il y a dans une case en fonction de paramètres indiquant la position dans le tableau
    def getCase(self, ligne : int, col : int):
        return self.__affichage[ligne][col]

    # permet de récupérer la valeur de l'attribut perdu
    @property
    def getPerdu(self) -> int:
        return self.__perdu
    
    # permet de récupérer la valeur de l'attribut gagne
    @property
    def getGagne(self) -> int:
        return self.__gagne
    
    # permet de récupérer la valeur de l'attribut nbAffichage
    @property
    def getNbAffichage(self) -> int:
        return self.__nbAffichage

