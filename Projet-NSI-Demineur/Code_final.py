import pygame
from pygame import*
from random import*
from math import*
import sys


class Case:

    def __init__(self):
        '''entrée = un objet instancié de la classe Case

            sortie = self._case, un dictionnaire qui répertorie toutes les informations de l'objet'''

        self._case = {"decouverte" : False, "bombe" : False, "drapeau" : False}

    def case(self):
        '''entrée = un objet de la classe Case

            sortie = l'objet pris en paramètre'''

        return self._case

    def decouvrir(self):
        '''entrée = un objet de la classe Case

            traitement = change le booléen de la clé decouverte en True

            sortie = l'objet pris en paramètre'''

        self._case["decouverte"] = True
        return self._case

    def bombe(self):
        '''entrée = un objet de la classe Case

            traitement = change le booléen de la clé bombe en True

            sortie = l'objet pris en paramètre'''

        self._case["bombe"] = True
        return self._case

    def drapeau(self):
        '''entrée = un objet de la classe Case

            traitement = change le booléen de la clé drapeau en True

            sortie = l'objet pris en paramètre'''

        self._case["drapeau"] = True
        return self._case

    def delete(self):
        '''entrée = un objet de la classe Case

            traitement = change le booléen de toutes les clés en False

            sortie = l'objet pris en paramètre'''

        self._case = {"decouverte" : False, "bombe" : False, "drapeau" : False}
        return self._case

    def drapeau_bombe(self):
        '''entrée = un objet de la classe Case

            traitement = change le booléen des clés drapeau et bombe en True

            sortie = l'objet pris en paramètre'''

        self._case["drapeau"] = True
        self._case["bombe"] = True
        return self._case

    def bombe_decouverte(self):
        '''entrée = un objet de la classe Case

            traitement = change le booléen des clés decouverte et bombe en True

            sortie = l'objet pris en paramètre'''

        self._case["decouverte"] = True
        self._case["bombe"] = True
        return self._case


class Grille:

    def __init__(self, n, bombes, pixels):
        '''entrée = l'objet instancié de la class Grille, n pour la taille de la grille(n x n),
                    bombes pour le nombre de bombes sur le terrain, pixels pour la taille des images lors de l'affichage du jeu,

            sortie = self._drapeaux = bombes, self._liste utile à la méthode decouvrir_case,
                    self._infos qui regroupe tous les objets de la class Case (sous forme de grille),
                    self._numeros utile à la méthode calculer_numeros qui répertorie le nombre de chaque case en fonction des bombes autour (sous forme de grille)'''

        self._pixels = pixels
        self._taille = n
        self._bombes = bombes
        self._drapeaux = bombes
        self._liste = []
        self._infos = [[Case().case()] * n for i in range(n)]
        self._numeros = [[0] * n for i in range(n)]

    def decouvrir_case(self, l, c, file = []):
        '''entrée = la grille, la ligne et la colonne qu'on veut traiter, une liste file

            traitement = change le booléen de la clé decouverte dans le dictionnaire qu'on veut changer en True.
                            Si l'emplacement de la case qu'on souhaite découvrir est correspond à un 0 dans la grille des numeros, toutes les cases autour sont découvertes,
                            et si une des cases autour correspond à un 0 dans la grille des numeros, on ajoute ses coordonnées(l et c) dans la file, puis il sera traité quand la file sera vidée.

            sortie = un ou plusieurs objets de la class Case avec en booléen de la clé decouverte True'''

        if self._numeros[l][c] == 0:
            # on créer une file à la manière d'un parcours en largeur afin de s'occuper de toutes les case_0 autour d'une même case_0
            file.append([l, c])
            while len(file) != 0:
                # jusqu'à ce que toutes les cases_0 autour soient traitées
                case_0 = file.pop(0)
                # on défile une case_0 à proximité de la case_0 traité à l'origine
                self._liste.append(case_0)
                self._voisins_l = [case_0[0]]
                self._voisins_c = [case_0[1]]
                # on s'occupe de tous les cas possibles, si l'indice_l choisi est égal à 0 par exemple, on aura forcément aucune case en dessous, c'est une limite de la grille
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
        '''entrée = la grille, la ligne et la colonne qu'on veut traiter, un entier b = 0

            traitement = prend une case aléatoirement dans la grille et change son booléen de la clé bombe en True, l'opération est répétée plusieurs fois en fonction de b

            sortie =  plusieurs objets de la class Case avec en booléen de la clé bombe True'''

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
            # on s'assure que le nombre de bombes souhaité sur le terrain de jeu corresponde bien à ce qui est attendu(self._bombes)
            # car en choisissant plusieurs fois aléatoirement une case, on peut retomber sur la même et perdre une bombe.
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
        '''entrée = la grille

            traitement = parcours la grille des informations et si la cle bombe est égal à True dans un des cases parcourues,
                        on prend ses coordonnées(l et c) et on ajoute 1 dans tous les indices autour dans self._numeros.

            sortie =  self._numeros, la grille des numeros'''

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

    def marquer(self, l, c):
        '''entrée = la grille, la ligne et la colonne qu'on veut traiter

            traitement =  change la valeur de la cle drapeau de l'objet de la class Case en True.

            sortie =  la grille des infos avec le changement effectuer'''

        if self._infos[l][c]['bombe'] == True:
            if self._drapeaux != 0:
                self._infos[l][c] = Case().drapeau_bombe()
                self._drapeaux -= 1
        elif self._infos[l][c]['decouverte'] == False:
            if self._drapeaux != 0:
                self._infos[l][c] = Case().drapeau()
                self._drapeaux -= 1

    def demarquer(self, l, c):
        '''entrée = la grille, la ligne et la colonne qu'on veut traiter

            traitement =  change la valeur de la cle drapeau de l'objet de la class Case en False.

            sortie =  la grille des infos avec le changement effectuer'''

        if self._infos[l][c]['bombe'] and self._infos[l][c]['drapeau'] == True:
            self._infos[l][c] = Case().bombe()
            self._drapeaux += 1
        elif self._infos[l][c]['drapeau'] == True:
            self._infos[l][c] = Case().delete()
            self._drapeaux += 1

    def gagner(self):
        '''entrée = la grille

            traitement =  parcours la grille des infos et si une case bombe a par dessus un drapeau, on ajoute 1 à un compteur qu'on créer au début.
                            Si à la fin le compteur est égal à self._bombes(le nombre de bombes sur le terrain), l'attribut gagner = False est changé en True.

            sortie =  l'attribut gagner'''

        gagner = False
        compteur = 0
        for ligne in self._infos:
            for colonne in ligne:
                if colonne['decouverte'] == True:
                    compteur += 1
        if compteur == self._taille**2 - self._bombes:
            gagner = True
            return gagner

    def perdre(self):
        '''entrée = la grille

            traitement =  parcours la grille des infos et si une case bombe est decouverte, on reparcours la grille est infos pour decouvrir toutes les autres cases bombe.
                            l'attribut perdre = False est changé en True.

            sortie =  l'attribut perdre'''

        perdre = False
        # comme pour la méthode decouvrir_case, on créer une file qui va permettre de parcourir toutes les bombes du terrain
        self._file = []
        l = 0
        for ligne in self._infos:
            c = 0
            for colonne in ligne:
                if colonne['bombe'] and colonne['decouverte'] == True:
                    indice = [l, c]
                    self._file.append(indice)
                    # ajouter en tant que premier élément de la file l'indice de la bombe sur laquelle on a cliqué est important pour que la révélation des toutes les bombes soit cohérente
                    l = 0
                    for ligne in self._infos:
                        c = 0
                        for colonne in ligne:
                            if colonne['bombe'] == True and colonne['decouverte'] == False:
                                indice = [l, c]
                                self._file.append(indice)
                                colonne['decouverte'] = Case().bombe_decouverte()
                            c += 1
                        l += 1
                    perdre = True
                    return perdre
                c += 1
            l += 1

    def jouer(self):

        init()

        clock = time.Clock()
        time.set_timer(USEREVENT, 1000)

        fenetre = display.set_mode((1535, 800))
        display.set_caption('Démineur')

        secs = 0
        min = 0
        heures = 0

        font = pygame.font.SysFont('Consolas', 32)
        font2 = pygame.font.SysFont('Consolas', 60)
        # mise en forme de l'affichage du temps dans le jeu
        text = font.render('{}:{}:{}'.format(heures, min, secs), True, (255, 255, 255), (0, 0, 0))

        images = {'box' : image.load('box.png'), 'decouverte' : image.load('decouverte.png'),
                'box_flag' : image.load('box_flag.png'), 'flag' : image.load('flag.png'), 'case_1' : image.load('case_1.png'),
                'case_2' : image.load('case_2.png'), 'case_3' : image.load('case_3.png'), 'case_4' : image.load('case_4.png'),
                'case_5' : image.load('case_5.png'), 'case_6' : image.load('case_6.png'), 'case_7' : image.load('case_7.png'),
                'case_8' : image.load('case_8.png')}

        # on créer un liste qui garde toutes les images de l'animation de l'explosion
        images_e = [image.load('e_1.png'), image.load('e_2.png'), image.load('e_3.png'),
                    image.load('e_4.png'), image.load('e_5.png'), image.load('e_6.png'),
                    image.load('e_7.png'), image.load('e_8.png'), image.load('e_9.png'),
                    image.load('e_10.png'), image.load('e_11.png'), image.load('e_12.png')]

        images_e_scale = []

        for image_e in images_e:
            image_e = transform.scale(image_e, (self._pixels, self._pixels))
            images_e_scale += [image_e]

        images_e = images_e_scale

        for cle, valeur in images.items():
            valeur = transform.scale(valeur, (self._pixels, self._pixels))
            images[cle] = valeur
        images['flag'] = transform.scale(images['flag'], (100, 100))

        # ici, on a redimensionné toutes les images des cases en fonction de la difficulté du jeu, selon lequel self._pixels sera différent ( + de cases = - de pixels)

        # la variable timer sert à mettre en route le temps après un premier clic
        timer = False
        continuer = True
        # la variable action sert à ce qu'on ne puisse plus interragir avec la grille une fois la partie terminée
        action = True

        while continuer:

            for events in event.get():

                if events.type == QUIT:
                    continuer = False

                if self.gagner():
                    fenetre.blit(text3, (900, 100))
                    timer = False
                    action = False
                if self.perdre():
                    fenetre.blit(text4, (900, 100))
                    timer = False
                    action = False
                    while len(self._file) != 0:
                        # on s'occupe d'animer toutes les explosions (toutes les cases bombe)
                        indice = self._file.pop(0)
                        for i in range(len(images_e)):
                            # on parcours toutes images dans un ordre précis afin d'assurer l'animation
                            time.delay(75)
                            fenetre.blit(images_e[i], (indice[1]*self._pixels, indice[0]*self._pixels))
                            display.update()
                        # après la première animation qui correspond à la case bombe sur laquelle on a cliqué, on mélange la file afin que la révélation des bombes se fasse aléatoirement
                        shuffle(self._file)
                    continuer = False

                if events.type == USEREVENT:
                    fenetre.blit(text, (950, 650))
                    if timer == True:
                        secs += 1
                        if secs == 60:
                            secs = 0
                            min += 1
                        if min == 60:
                            min = 0
                            heures += 1
                        text = font.render('{}:{}:{}'.format(heures, min, secs), True, (255, 255, 255), (0, 0, 0))

                fenetre.blit(images['flag'], (900, 350))
                text2 = font.render(' = {}'.format(self._drapeaux), True, (255, 255, 255), (0, 0, 0))
                fenetre.blit(text2, (1000, 380))
                text3 = font2.render('Vous avez gagné !', True, (0, 255, 0), (0, 0, 0))
                text4 = font2.render('Vous avez perdu !', True, (255, 0, 0), (0, 0, 0))

                l = 0
                y = 0
                for ligne in self._infos:
                    c = 0
                    x = 0
                    for colonne in ligne:
                        if colonne['decouverte'] == False:
                            fenetre.blit(images['box'], (x,y))
                        if colonne['drapeau'] == True :
                            fenetre.blit(images['box_flag'], (x,y))
                        if colonne['decouverte'] == True and colonne['bombe'] == False:
                            if self._numeros[l][c] == 0:
                                fenetre.blit(images['decouverte'], (x,y))
                            if self._numeros[l][c] == 1:
                                fenetre.blit(images['case_1'], (x,y))
                            if self._numeros[l][c] == 2:
                                fenetre.blit(images['case_2'], (x,y))
                            if self._numeros[l][c] == 3:
                                fenetre.blit(images['case_3'], (x,y))
                            if self._numeros[l][c] == 4:
                                fenetre.blit(images['case_4'], (x,y))
                            if self._numeros[l][c] == 5:
                                fenetre.blit(images['case_5'], (x,y))
                            if self._numeros[l][c] == 6:
                                fenetre.blit(images['case_6'], (x,y))
                            if self._numeros[l][c] == 7:
                                fenetre.blit(images['case_7'], (x,y))
                            if self._numeros[l][c] == 8:
                                fenetre.blit(images['case_8'], (x,y))
                        c += 1
                        x += self._pixels
                    l += 1
                    y += self._pixels
                display.flip()

                if mouse.get_pressed()[0]:
                    if events.type == MOUSEBUTTONDOWN:
                        pos=mouse.get_pos()
                        # pour que la clic soit pris en compte, il faut qu'il se fasse uniquement sur la grille
                        if pos[0]//self._pixels < self._taille:
                            if action == True:
                                timer = True
                                # on parcours la grille des informations afin de savoir s'il y a des bombes ou pas (sinon, c'est la premier clic)
                                b = 0
                                for ligne in self._infos:
                                    for colonne in ligne:
                                        if colonne['bombe'] == True:
                                            b += 1
                                if b == 0:
                                    self.placement_bombes(pos[1]//self._pixels, pos[0]//self._pixels)
                                    self.calculer_numeros()
                                self.decouvrir_case(pos[1]//self._pixels, pos[0]//self._pixels)

                if mouse.get_pressed()[2]:
                    if events.type == MOUSEBUTTONDOWN:
                        pos=mouse.get_pos()
                        if pos[0]//self._pixels < self._taille:
                            if action == True:
                                if self._infos[pos[1]//self._pixels][pos[0]//self._pixels]['drapeau'] == True:
                                    self.demarquer(pos[1]//self._pixels, pos[0]//self._pixels)
                                elif self._infos[pos[1]//self._pixels][pos[0]//self._pixels]['drapeau'] == False:
                                    self.marquer(pos[1]//self._pixels, pos[0]//self._pixels)

            clock.tick(60)

        quit()
        sys.exit()


class Menu:

    def difficultes(self):

        init()
        fenetre = display.set_mode((1400, 700))
        display.set_caption('Démineur')

        font = pygame.font.SysFont('Consolas', 60)

        images = {'facile' : image.load('facile.png'), 'moyen' : image.load('moyen.png'), 'difficile' : image.load('difficile.png')}

        for cle, valeur in images.items():
            valeur = transform.scale(valeur, (100, 100))
            images[cle] = valeur

        x = 100
        y = 400
        for i in images:
            fenetre.blit(images[i], (x, y))
            x += 500

        text = font.render('Choisir la difficulté:', True, (255, 255, 255), (0, 0, 0))
        fenetre.blit(text, (100, 100))

        continuer = True
        while continuer:
            for events in event.get():
                if mouse.get_pressed()[0]:
                    if events.type == MOUSEBUTTONDOWN:
                        pos=mouse.get_pos()
                        if pos[1]//100 == 4:
                            # on définit les difficultés
                            if pos[0]//100 == 1:
                                self._taille = 8
                                self._bombes = 10
                                self._pixels = 80
                                g = Grille(self._taille, self._bombes, self._pixels)
                                g.jouer()
                            if pos[0]//100 == 6:
                                self._taille = 14
                                self._bombes = 40
                                self._pixels = 50
                                g = Grille(self._taille, self._bombes, self._pixels)
                                g.jouer()
                            if pos[0]//100 == 11:
                                self._taille = 20
                                self._bombes = 99
                                self._pixels = 35
                                g = Grille(self._taille, self._bombes, self._pixels)
                                g.jouer()
                    if events.type == QUIT:
                        continuer = False
            display.flip()
        quit()
        sys.exit()


Menu().difficultes()


