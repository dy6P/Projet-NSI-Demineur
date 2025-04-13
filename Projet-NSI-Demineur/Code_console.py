from pygame import*
from random import*
from math import*


class Case:

    def __init__(self):
        self._case = {"decouverte" : False, "bombe" : False, "drapeau" : False}

    def case(self):
        return self._case

    def decouvrir(self):
        self._case["decouverte"] = True
        return self._case

    def bombe(self):
        self._case["bombe"] = True
        return self._case

    def drapeau(self):
        self._case["drapeau"] = True
        return self._case

    def delete(self):
        self._case = {"decouverte" : False, "bombe" : False, "drapeau" : False}
        return self._case

    def drapeau_bombe(self):
        self._case["drapeau"] = True
        self._case["bombe"] = True
        return self._case

    def bombe_decouverte(self):
        self._case["decouverte"] = True
        self._case["bombe"] = True
        return self._case


class Grille:

    def __init__(self, n, bombes):
        self._taille = n
        self._bombes = bombes
        self._drapeaux = bombes
        self._liste = []
        self._infos = [[Case().case()] * n for i in range(n)]
        self._numeros = [[0] * n for i in range(n)]
        self._grille = [["■"] * n for i in range(n)]

    def decouvrir_case(self, l, c, file = []):
        if self._numeros[l][c] == 0:
            file.append([l, c])
            while len(file) != 0:
                case_0 = file.pop(0)
                self._liste.append(case_0)
                self._voisins_l = [case_0[0]]
                self._voisins_c = [case_0[1]]
                if case_0[1] > 0:
                    self._voisins_c.append(case_0[1] - 1)
                if case_0[1] < self._taille - 1:
                    self._voisins_c.append(case_0[1] + 1)
                if case_0[0] > 0:
                    self._voisins_l.append(case_0[0] - 1)
                if case_0[0] < self._taille - 1:
                    self._voisins_l.append(case_0[0] + 1)
                for i_l in self._voisins_l:
                    for i_c in self._voisins_c:
                        if self._infos[i_l][i_c]['bombe'] == True:
                            self._infos[i_l][i_c] = Case().bombe_decouverte()
                        else:
                            if self._infos[i_l][i_c]['drapeau'] == True:
                                self._drapeaux += 1
                            self._infos[i_l][i_c] = Case().decouvrir()
                        if self._numeros[i_l][i_c] == 0:
                            if [i_l, i_c] not in self._liste:
                                file.append([i_l, i_c])
        else:
            if self._infos[l][c]['bombe'] == True:
                self._infos[l][c] = Case().bombe_decouverte()
            else:
                if self._infos[l][c]['drapeau'] == True:
                    self._drapeaux += 1
                self._infos[l][c] = Case().decouvrir()

    def placement_bombes(self, l, c, b = 0):
        self._voisins_c = [c]
        self._voisins_l = [l]
        if c > 0:
            self._voisins_c.append(c - 1)
        if c < self._taille - 1:
            self._voisins_c.append(c + 1)
        if l > 0:
            self._voisins_l.append(l - 1)
        if l < self._taille - 1:
            self._voisins_l.append(l + 1)
        while b != self._bombes:
            b = 0
            i_l = randrange(self._taille)
            i_c = randrange(self._taille)
            if i_l not in self._voisins_l or i_c not in self._voisins_c:
                self._infos[i_l][i_c] = Case().bombe()
            for ligne in self._infos:
                for colonne in ligne:
                    if colonne['bombe'] == True:
                        b += 1

    def calculer_numeros(self):
        l = 0
        for ligne in self._infos:
            c = 0
            for colonne in ligne:
                if colonne['bombe'] == True:
                    self._numeros[l][c] = 1
                    self._voisins_l = [l]
                    self._voisins_c = [c]
                    if c > 0:
                        self._voisins_c.append(c - 1)
                    if c < self._taille - 1:
                        self._voisins_c.append(c + 1)
                    if l > 0:
                        self._voisins_l.append(l - 1)
                    if l < self._taille - 1:
                        self._voisins_l.append(l + 1)
                    for i_l in self._voisins_l:
                        for i_c in self._voisins_c:
                            self._numeros[i_l][i_c] += 1
                c += 1
            l += 1

    def grille(self):
        l = 0
        for ligne in self._infos:
            c = 0
            for colonne in ligne:
                if colonne['decouverte'] == False:
                    self._grille[l][c] = "■"
                if colonne['drapeau'] == True:
                    self._grille[l][c] = "X"
                if colonne['decouverte'] == True:
                    self._grille[l][c] = str(self._numeros[l][c])
                if colonne['bombe'] and colonne['decouverte'] == True:
                    self._grille[l][c] = "B"
                c += 1
            l += 1

    def marquer(self, l, c):
        if self._infos[l][c]['bombe'] == True:
            if self._drapeaux != 0:
                self._infos[l][c] = Case().drapeau_bombe()
                self._drapeaux -= 1
        elif self._infos[l][c]['decouverte'] == False:
            if self._drapeaux != 0:
                self._infos[l][c] = Case().drapeau()
                self._drapeaux -= 1

    def demarquer(self, l, c):
        if self._infos[l][c]['bombe'] and self._infos[l][c]['drapeau'] == True:
            self._infos[l][c] = Case().bombe()
            self._drapeaux += 1
        elif self._infos[l][c]['drapeau'] == True:
            self._infos[l][c] = Case().delete()
            self._drapeaux += 1

    def gagner(self):
        gagner = False
        compteur = 0
        for ligne in self._infos:
            for colonne in ligne:
                if colonne['drapeau'] and colonne['bombe'] == True:
                    compteur += 1
        if compteur == self._bombes:
            gagner = True
            return gagner

    def perdre(self):
        perdre = False
        for ligne in self._infos:
            for colonne in ligne:
                if colonne['bombe'] and colonne['decouverte'] == True:
                    for ligne in self._infos:
                        for colonne in ligne:
                            if colonne['bombe'] == True:
                                colonne['decouverte'] = Case().bombe_decouverte()
                    perdre = True
                    return perdre

    def afficher_infos(self):
        print(">")
        for ligne in self._infos:
            print(ligne)

    def afficher_numeros(self):
        print(">")
        for ligne in self._numeros:
            print(ligne)

    def afficher_grille(self):
        print(">")
        for ligne in self._grille:
            print(ligne)


class Jeu:

    def __init__(self):
        self._reponses_possibles = ["facile", "moyen", "difficile"]
        self._indices_possibles = []
        self._actions_possibles = ["a", "e", "d"]
        self._fin = False

    def difficulte(self):
        self._difficulte = input("Choisir la difficulté -> facile | moyen | difficile -> ")
        while self._difficulte not in self._reponses_possibles:
            self._difficulte = input("-> Choisir une des difficultés proposées (facile, moyen, difficile) -> ")
        if self._difficulte == "facile":
            self._taille = 8
            self._bombes = 10
        if self._difficulte == "moyen":
            self._taille = 14
            self._bombes = 40
        if self._difficulte == "difficile":
            self._taille = 20
            self._bombes = 80
        g = Grille(self._taille, self._bombes)
        g.afficher_grille()
        self.jouer(g, self._taille)

    def jouer(self, grille, n):
        self._indices_possibles = [i for i in range(n)]
        self._choix_indice_l = int(input("Choisir l'indice d'une ligne de la grille -> "))
        while self._choix_indice_l not in self._indices_possibles:
            self._choix_indice_l = int(input("Choisir l'indice d'une ligne de la grille -> (entre 0 et " + str(n-1) + ") -> "))
        self._choix_indice_c = int(input("Choisir l'indice d'une colonne de la ligne -> "))
        while self._choix_indice_c not in self._indices_possibles:
            self._choix_indice_c = int(input("Choisir l'indice d'une colonne de la ligne -> (entre 0 et " + str(n-1) + ") -> "))
        grille.placement_bombes(self._choix_indice_l, self._choix_indice_c)
        grille.calculer_numeros()
        grille.decouvrir_case(self._choix_indice_l, self._choix_indice_c)
        grille.grille()
        grille.afficher_grille()
        while self._fin == False:
            self._choix_actions = input("Ajouter un drapeau avec la touche a | Enlever un drapeau avec la touche e | Découvrir une case avec la touche d -> ")
            while self._choix_actions not in self._actions_possibles:
                self._choix_actions = input("Ajouter un drapeau avec la touche a | Enlever un drapeau avec la touche e | Découvrir une case avec la touche d -> ")
            self._choix_indice_l = int(input("Choisir l'indice d'une ligne de la grille -> "))
            while self._choix_indice_l not in self._indices_possibles:
                self._choix_indice_l = int(input("Choisir l'indice d'une ligne de la grille -> (entre 0 et " + str(n-1) + ") -> "))
            self._choix_indice_c = int(input("Choisir l'indice d'une colonne de la ligne -> "))
            while self._choix_indice_c not in self._indices_possibles:
                self._choix_indice_c = int(input("Choisir l'indice d'une colonne de la ligne -> (entre 0 et " + str(n-1) + ") -> "))
            if self._choix_actions == "a":
                grille.marquer(self._choix_indice_l, self._choix_indice_c)
            if self._choix_actions == "e":
                grille.demarquer(self._choix_indice_l, self._choix_indice_c)
            if self._choix_actions == "d":
                grille.decouvrir_case(self._choix_indice_l, self._choix_indice_c)
            if grille.gagner():
                print("Vous avez gagné.")
                self._fin = grille.gagner()
            if grille.perdre():
                print("Vous avez perdu.")
                self._fin = grille.perdre()
            grille.grille()
            grille.afficher_grille()




jeu = Jeu()
jeu.difficulte()


