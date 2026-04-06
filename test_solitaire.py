#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from solitaire_cipher import Solitaire, SolitaireSimple, creer_paquet_melange


def afficher_resultat(nom_test, ok):
    statut = "OK" if ok else "ECHEC"
    print(f"{nom_test:<60} [{statut}]")
    return ok


def test_chiffrement_dechiffrement_complet():
    message = "BONJOUR"

    expediteur = Solitaire()
    destinataire = Solitaire()

    chiffre = expediteur.chiffrer(message)
    dechiffre = destinataire.dechiffrer(chiffre)

    return afficher_resultat("Test 1 - chiffrement/déchiffrement complet", dechiffre == message)


def test_chiffrement_dechiffrement_simple():
    message = "BONJOUR"

    expediteur = SolitaireSimple()
    destinataire = SolitaireSimple()

    chiffre = expediteur.chiffrer(message)
    dechiffre = destinataire.dechiffrer(chiffre)

    return afficher_resultat("Test 2 - chiffrement/déchiffrement simple", dechiffre == message)


def test_messages_successifs_complet():
    """
    Le deuxième message doit utiliser l'état du paquet laissé par le premier.
    """
    msg1 = "AVANT"
    msg2 = "APRES"

    expediteur = Solitaire()
    destinataire = Solitaire()

    chiffre1 = expediteur.chiffrer(msg1)
    chiffre2 = expediteur.chiffrer(msg2)

    dechiffre1 = destinataire.dechiffrer(chiffre1)
    dechiffre2 = destinataire.dechiffrer(chiffre2)

    ok = (dechiffre1 == msg1) and (dechiffre2 == msg2)
    return afficher_resultat("Test 3 - messages successifs complet", ok)


def test_messages_successifs_simple():
    """
    Même idée pour la version simplifiée.
    """
    msg1 = "SECRET"
    msg2 = "MISSION"

    expediteur = SolitaireSimple()
    destinataire = SolitaireSimple()

    chiffre1 = expediteur.chiffrer(msg1)
    chiffre2 = expediteur.chiffrer(msg2)

    dechiffre1 = destinataire.dechiffrer(chiffre1)
    dechiffre2 = destinataire.dechiffrer(chiffre2)

    ok = (dechiffre1 == msg1) and (dechiffre2 == msg2)
    return afficher_resultat("Test 4 - messages successifs simple", ok)


def test_paquet_melange_reproductible():
    """
    Avec la même graine, on doit obtenir le même paquet.
    """
    p1 = creer_paquet_melange(42)
    p2 = creer_paquet_melange(42)
    p3 = creer_paquet_melange(99)

    ok = (p1 == p2) and (p1 != p3)
    return afficher_resultat("Test 5 - paquet mélangé reproductible", ok)


def test_reinitialisation_paquet():
    """
    Vérifie que reinitialiser() remet bien le paquet à son état de départ.
    """
    s = Solitaire(creer_paquet_melange(7))
    etat_initial = s.etat_paquet()

    _ = s.chiffrer("BONJOUR")
    s.reinitialiser()

    ok = s.etat_paquet() == etat_initial
    return afficher_resultat("Test 6 - réinitialisation du paquet", ok)


def test_reutilisation_flux_apres_reinitialisation_complet():
    """
    Après réinitialisation avec le même paquet initial, on retrouve le même
    début de flux. Ce test montre pourquoi il ne faut pas réinitialiser entre
    deux messages d'une même communication.
    """
    s = Solitaire(creer_paquet_melange(11))

    chiffre1 = s.chiffrer("BONJOUR")
    s.reinitialiser()
    chiffre2 = s.chiffrer("BONJOUR")

    ok = chiffre1 == chiffre2
    return afficher_resultat("Test 7 - même flux après réinitialisation complet", ok)


def test_reutilisation_flux_apres_reinitialisation_simple():
    """
    Même démonstration pour la version simplifiée.
    """
    s = SolitaireSimple(creer_paquet_melange(11))

    chiffre1 = s.chiffrer("BONJOUR")
    s.reinitialiser()
    chiffre2 = s.chiffrer("BONJOUR")

    ok = chiffre1 == chiffre2
    return afficher_resultat("Test 8 - même flux après réinitialisation simple", ok)


def test_meme_message_sans_reinitialisation_donne_resultat_different():
    """
    Si on rechiffre le même message sans réinitialiser, le résultat doit être
    différent car le paquet a avancé.
    """
    s = Solitaire()

    chiffre1 = s.chiffrer("BONJOUR")
    chiffre2 = s.chiffrer("BONJOUR")

    ok = chiffre1 != chiffre2
    return afficher_resultat("Test 9 - même message, flux différent sans reset", ok)


def lancement_des_tests():
    print("=" * 72)
    print("TESTS DU PROJET SOLITAIRE")
    print("=" * 72)

    resultats = [
        test_chiffrement_dechiffrement_complet(),
        test_chiffrement_dechiffrement_simple(),
        test_messages_successifs_complet(),
        test_messages_successifs_simple(),
        test_paquet_melange_reproductible(),
        test_reinitialisation_paquet(),
        test_reutilisation_flux_apres_reinitialisation_complet(),
        test_reutilisation_flux_apres_reinitialisation_simple(),
        test_meme_message_sans_reinitialisation_donne_resultat_different(),
    ]

    total = len(resultats)
    reussis = sum(resultats)

    print("-" * 72)
    print(f"Résultat final : {reussis}/{total} tests réussis")
    print("=" * 72)

    if all(resultats):
        print("Tous les tests sont validés.")
    else:
        print("Certains tests ont échoué.")


if __name__ == "__main__":
    lancement_des_tests()