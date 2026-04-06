#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Démonstration console du chiffrement Solitaire.

Cette démo respecte les consignes du sujet :
- un expéditeur et un destinataire partent du même paquet initial ;
- les messages successifs utilisent l'état du paquet laissé par le message précédent ;
- il ne faut pas réinitialiser entre deux messages d'une même communication,
  sinon on rejoue le même début de flux de clé.
"""

from solitaire_cipher import Solitaire, SolitaireSimple, creer_paquet_melange


def afficher_menu():
    print("\n" + "=" * 60)
    print("DEMONSTRATION DU CHIFFREMENT SOLITAIRE")
    print("=" * 60)
    print("1. Initialiser une communication")
    print("2. Chiffrer un message")
    print("3. Déchiffrer un message")
    print("4. Voir l'état courant du paquet")
    print("5. Démarrer une nouvelle communication")
    print("6. Démonstration des 5 opérations")
    print("7. Quitter")


def choisir_version():
    print("\nChoix de la version :")
    print("1. Complète")
    print("2. Simplifiée")

    choix = input("Votre choix (1-2) : ").strip()
    return "complete" if choix == "1" else "simple"


def choisir_paquet():
    print("\nChoix du paquet initial :")
    print("1. Séquentiel (1,2,3,...,54)")
    print("2. Mélangé avec une graine")

    choix = input("Votre choix (1-2) : ").strip()

    if choix == "2":
        try:
            graine = int(input("Entrez une graine entière : ").strip())
            return creer_paquet_melange(graine)
        except ValueError:
            print("Graine invalide. On utilise le paquet séquentiel.")
            return None

    return None


def creer_chiffreur(version, paquet):
    if version == "complete":
        return Solitaire(paquet)
    return SolitaireSimple(paquet)


def initialiser_communication():
    version = choisir_version()
    paquet = choisir_paquet()

    expediteur = creer_chiffreur(version, paquet)
    destinataire = creer_chiffreur(version, paquet)

    print("\nCommunication initialisée.")
    print("Les deux correspondants possèdent le même paquet de départ.")
    print("Ne réinitialisez pas entre deux messages d'une même conversation.")
    return version, paquet, expediteur, destinataire


def chiffrer_message(expediteur):
    message = input("\nMessage à chiffrer : ").strip()
    if not message:
        print("Message vide.")
        return

    chiffre = expediteur.chiffrer(message)
    print(f"Message chiffré : {chiffre}")


def dechiffrer_message(destinataire):
    message = input("\nMessage chiffré à déchiffrer : ").strip()
    if not message:
        print("Message vide.")
        return

    dechiffre = destinataire.dechiffrer(message)
    print(f"Message déchiffré : {dechiffre}")


def voir_etat_paquet(expediteur, destinataire):
    print("\nEtat du paquet côté expéditeur (20 premières cartes) :")
    print(expediteur.etat_paquet()[:20], "...")
    print("\nEtat du paquet côté destinataire (20 premières cartes) :")
    print(destinataire.etat_paquet()[:20], "...")


def demo_operations():
    cipher = Solitaire()

    print("\n" + "=" * 60)
    print("DEMONSTRATION DES 5 OPERATIONS")
    print("=" * 60)
    print("Paquet initial (15 premières cartes) :")
    print(cipher.etat_paquet()[:15], "...")

    input("\nAppuyez sur Entrée pour l'opération 1...")
    cipher.operation1_joker_noir()
    print("Après joker noir :")
    print(cipher.etat_paquet()[:15], "...")

    input("\nAppuyez sur Entrée pour l'opération 2...")
    cipher.operation2_joker_rouge()
    print("Après joker rouge :")
    print(cipher.etat_paquet()[:15], "...")

    input("\nAppuyez sur Entrée pour l'opération 3...")
    cipher.operation3_double_coupe()
    print("Après double coupe :")
    print(cipher.etat_paquet()[:15], "...")

    input("\nAppuyez sur Entrée pour l'opération 4...")
    cipher.operation4_coupe_simple()
    print("Après coupe simple :")
    print(cipher.etat_paquet()[:15], "...")

    input("\nAppuyez sur Entrée pour l'opération 5...")
    lettre = cipher.operation5_lecture()
    if lettre is None:
        print("Lecture sur un joker : il faut recommencer un cycle complet.")
    else:
        print(f"Valeur lue : {lettre}")


def main():
    version = None
    paquet = None
    expediteur = None
    destinataire = None

    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()

        if choix == "1":
            version, paquet, expediteur, destinataire = initialiser_communication()

        elif choix == "2":
            if expediteur is None:
                print("Commencez par initialiser une communication.")
            else:
                chiffrer_message(expediteur)

        elif choix == "3":
            if destinataire is None:
                print("Commencez par initialiser une communication.")
            else:
                dechiffrer_message(destinataire)

        elif choix == "4":
            if expediteur is None or destinataire is None:
                print("Commencez par initialiser une communication.")
            else:
                voir_etat_paquet(expediteur, destinataire)

        elif choix == "5":
            if expediteur is None or destinataire is None:
                print("Commencez par initialiser une communication.")
            else:
                expediteur.reinitialiser()
                destinataire.reinitialiser()
                print("Nouvelle communication démarrée depuis le paquet initial.")
                print("Attention : cela rejoue le début du flux de clé.")

        elif choix == "6":
            demo_operations()

        elif choix == "7":
            print("Au revoir.")
            break

        else:
            print("Choix invalide.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterruption utilisateur. Au revoir.")