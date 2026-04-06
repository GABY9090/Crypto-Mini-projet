#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

JOKER_NOIR = 53
JOKER_ROUGE = 54
TAILLE_PAQUET = 54


def verifier_paquet(paquet):
    if not isinstance(paquet, list):
        raise TypeError("Le paquet doit être une liste.")
    if len(paquet) != TAILLE_PAQUET:
        raise ValueError("Le paquet doit contenir exactement 54 cartes.")
    if sorted(paquet) != list(range(1, TAILLE_PAQUET + 1)):
        raise ValueError("Le paquet doit contenir une seule fois chaque carte de 1 à 54.")


def creer_paquet_melange(graine=None):
    paquet = list(range(1, TAILLE_PAQUET + 1))
    rng = random.Random(graine)
    rng.shuffle(paquet)
    return paquet


def nettoyer_texte(texte):
    return "".join(c for c in texte.upper() if c.isalpha())


def texte_vers_nombres(texte):
    texte = nettoyer_texte(texte)
    return [ord(c) - ord("A") + 1 for c in texte]


def nombres_vers_texte(nombres):
    return "".join(chr(n - 1 + ord("A")) for n in nombres)


class Solitaire:
    """
    Version complète du chiffrement Solitaire.

    Point important du sujet : on ne doit pas réutiliser le même flux de clé
    pour deux messages successifs. Cela signifie que l'état du paquet doit être
    conservé d'un message au suivant tant qu'on reste dans la même communication.
    """

    def __init__(self, paquet=None):
        if paquet is None:
            self.paquet = list(range(1, TAILLE_PAQUET + 1))
        else:
            verifier_paquet(paquet)
            self.paquet = paquet.copy()

        self.paquet_initial = self.paquet.copy()

    def reinitialiser(self):
        """
        Redémarre une nouvelle communication depuis le paquet initial.

        Attention : si on réutilise exactement le même paquet initial, on
        retrouve le même début de flux de clé. Cette méthode ne doit donc pas
        être utilisée entre deux messages d'une même conversation secrète.
        """
        self.paquet = self.paquet_initial.copy()

    def etat_paquet(self):
        return self.paquet.copy()

    def operation1_joker_noir(self):
        pos = self.paquet.index(JOKER_NOIR)

        if pos == TAILLE_PAQUET - 1:
            self.paquet.pop(pos)
            self.paquet.insert(1, JOKER_NOIR)
        else:
            self.paquet[pos], self.paquet[pos + 1] = self.paquet[pos + 1], self.paquet[pos]

    def operation2_joker_rouge(self):
        pos = self.paquet.index(JOKER_ROUGE)
        self.paquet.pop(pos)

        if pos == TAILLE_PAQUET - 1:
            nouvelle_pos = 2
        elif pos == TAILLE_PAQUET - 2:
            nouvelle_pos = 1
        else:
            nouvelle_pos = pos + 2

        self.paquet.insert(nouvelle_pos, JOKER_ROUGE)

    def operation3_double_coupe(self):
        pos_noir = self.paquet.index(JOKER_NOIR)
        pos_rouge = self.paquet.index(JOKER_ROUGE)

        premier = min(pos_noir, pos_rouge)
        dernier = max(pos_noir, pos_rouge)

        dessus = self.paquet[:premier]
        milieu = self.paquet[premier:dernier + 1]
        dessous = self.paquet[dernier + 1:]

        self.paquet = dessous + milieu + dessus

    def operation4_coupe_simple(self):
        derniere_carte = self.paquet[-1]
        n = 53 if derniere_carte in (JOKER_NOIR, JOKER_ROUGE) else derniere_carte

        haut = self.paquet[:n]
        milieu = self.paquet[n:-1]
        bas = self.paquet[-1]

        self.paquet = milieu + haut + [bas]

    def operation5_lecture(self):
        premiere_carte = self.paquet[0]
        n = 53 if premiere_carte in (JOKER_NOIR, JOKER_ROUGE) else premiere_carte

        carte_lue = self.paquet[n]

        if carte_lue in (JOKER_NOIR, JOKER_ROUGE):
            return None

        return ((carte_lue - 1) % 26) + 1

    def generer_lettre_cle(self):
        while True:
            self.operation1_joker_noir()
            self.operation2_joker_rouge()
            self.operation3_double_coupe()
            self.operation4_coupe_simple()

            lettre = self.operation5_lecture()
            if lettre is not None:
                return lettre

    def generer_cle(self, longueur):
        return [self.generer_lettre_cle() for _ in range(longueur)]

    def chiffrer(self, message):
        msg_nombres = texte_vers_nombres(message)
        cle = self.generer_cle(len(msg_nombres))

        resultat = []
        for m, k in zip(msg_nombres, cle):
            valeur = m + k
            if valeur > 26:
                valeur -= 26
            resultat.append(valeur)

        return nombres_vers_texte(resultat)

    def dechiffrer(self, message_chiffre):
        msg_nombres = texte_vers_nombres(message_chiffre)
        cle = self.generer_cle(len(msg_nombres))

        resultat = []
        for m, k in zip(msg_nombres, cle):
            valeur = m - k
            if valeur <= 0:
                valeur += 26
            resultat.append(valeur)

        return nombres_vers_texte(resultat)


class SolitaireSimple:
    """
    Version simplifiée du projet.

    Ici aussi, l'état du paquet est conservé entre deux messages afin d'éviter
    de rejouer le même flux de clé dans une même communication.
    """

    def __init__(self, paquet=None):
        if paquet is None:
            self.paquet = list(range(1, TAILLE_PAQUET + 1))
        else:
            verifier_paquet(paquet)
            self.paquet = paquet.copy()

        self.paquet_initial = self.paquet.copy()
        self.alternance = True

    def reinitialiser(self):
        """
        Redémarre la génération depuis l'état initial.

        Comme pour la version complète, cela relance le flux à son début.
        """
        self.paquet = self.paquet_initial.copy()
        self.alternance = True

    def etat_paquet(self):
        return self.paquet.copy()

    def generer_lettre_cle(self):
        premiere = self.paquet.pop(0)

        if self.alternance:
            self.paquet.append(premiere)
        else:
            self.paquet.insert(len(self.paquet) - 1, premiere)

        self.alternance = not self.alternance

        return ((premiere - 1) % 26) + 1

    def generer_cle(self, longueur):
        return [self.generer_lettre_cle() for _ in range(longueur)]

    def chiffrer(self, message):
        msg_nombres = texte_vers_nombres(message)
        cle = self.generer_cle(len(msg_nombres))

        resultat = []
        for m, k in zip(msg_nombres, cle):
            valeur = m + k
            if valeur > 26:
                valeur -= 26
            resultat.append(valeur)

        return nombres_vers_texte(resultat)

    def dechiffrer(self, message_chiffre):
        msg_nombres = texte_vers_nombres(message_chiffre)
        cle = self.generer_cle(len(msg_nombres))

        resultat = []
        for m, k in zip(msg_nombres, cle):
            valeur = m - k
            if valeur <= 0:
                valeur += 26
            resultat.append(valeur)

        return nombres_vers_texte(resultat)


if __name__ == "__main__":
    s = Solitaire()
    print("1er BONJOUR :", s.chiffrer("BONJOUR"))
    print("2e BONJOUR :", s.chiffrer("BONJOUR"))