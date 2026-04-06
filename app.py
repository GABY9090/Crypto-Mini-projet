#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
from solitaire_cipher import Solitaire, SolitaireSimple, creer_paquet_melange


st.set_page_config(
    page_title="Chiffrement Solitaire",
    page_icon="🃏",
    layout="wide",
)


def creer_cipher(version, paquet):
    if version == "Complète":
        return Solitaire(paquet)
    return SolitaireSimple(paquet)


def get_paquet_initial(choix_paquet, graine):
    if choix_paquet == "Mélangé":
        return creer_paquet_melange(graine)
    return None  # None => paquet séquentiel 1..54


def initialiser_communication(version, paquet):
    st.session_state.version_active = version
    st.session_state.paquet_initial = paquet.copy() if paquet is not None else None
    st.session_state.expediteur = creer_cipher(version, paquet)
    st.session_state.destinataire = creer_cipher(version, paquet)
    st.session_state.dernier_chiffre = ""
    st.session_state.derniere_cle = []
    st.session_state.message_a_dechiffrer = ""
    st.session_state.dernier_dechiffre = ""


if "expediteur" not in st.session_state:
    initialiser_communication("Complète", None)


st.title("🃏 Chiffrement Solitaire")
st.markdown("Algorithme de Bruce Schneier")
st.warning(
    "Dans le sujet, on ne doit pas réutiliser le même flux de clé pour deux messages. "
    "Des valeurs peuvent se répéter dans une clé, mais il ne faut pas redémarrer le flux "
    "au milieu d'une même communication."
)

with st.sidebar:
    st.header("Configuration")

    version = st.radio(
        "Version",
        ["Complète", "Simplifiée"],
        index=0 if st.session_state.version_active == "Complète" else 1,
    )

    st.markdown("---")
    st.subheader("Paquet de cartes")

    choix_paquet = st.radio(
        "Ordre initial :",
        ["Séquentiel (1,2,3,...,54)", "Mélangé"]
    )

    graine = 42
    if choix_paquet == "Mélangé":
        graine = st.number_input("Graine :", value=42, step=1)

    paquet_initial = get_paquet_initial(
        "Mélangé" if choix_paquet == "Mélangé" else "Séquentiel",
        graine,
    )

    if st.button("Démarrer une nouvelle communication", type="primary"):
        initialiser_communication(version, paquet_initial)
        st.success(
            "Nouvelle communication initialisée. Le flux de clé redémarre depuis le paquet choisi."
        )

    st.caption(
        "À utiliser pour recommencer une nouvelle conversation, pas entre deux messages "
        "d'une même communication secrète."
    )

expediteur = st.session_state.expediteur
destinataire = st.session_state.destinataire

tab1, tab2, tab3 = st.tabs(["Chiffrement", "Déchiffrement", "Info"])


with tab1:
    st.header("Chiffrer un message")
    st.caption("Le paquet de l'expéditeur avance après chaque chiffrement.")

    message = st.text_area("Message :", value="Bonjour", key="message_chiffrement")
    voir_cle = st.checkbox("Voir la clé générée")

    if st.button("Chiffrer"):
        msg_propre = "".join(c for c in message.upper() if c.isalpha())

        if not msg_propre:
            st.error("Entrez un message contenant au moins une lettre.")
        else:
            paquet_courant = expediteur.paquet.copy()

            if isinstance(expediteur, SolitaireSimple):
                temp = SolitaireSimple(paquet_courant)
                temp.alternance = expediteur.alternance
            else:
                temp = Solitaire(paquet_courant)

            cle = temp.generer_cle(len(msg_propre))
            chiffre = expediteur.chiffrer(message)

            st.session_state.dernier_chiffre = chiffre
            st.session_state.derniere_cle = cle
            st.session_state.message_a_dechiffrer = chiffre

            st.success("Message chiffré !")
            st.code(chiffre)

            if voir_cle:
                st.write(f"Clé produite pour ce message : {cle}")

            st.info(
                "Le message chiffré a été copié automatiquement dans l'onglet Déchiffrement. "
                "Le destinataire doit déchiffrer les messages dans le même ordre."
            )

    if st.session_state.dernier_chiffre:
        st.markdown("### Dernier résultat")
        st.write(f"Texte chiffré : `{st.session_state.dernier_chiffre}`")


with tab2:
    st.header("Déchiffrer un message")
    st.caption("Le destinataire doit déchiffrer les messages dans le même ordre que l'expéditeur.")

    message_chiffre = st.text_area(
        "Message chiffré :",
        key="message_a_dechiffrer",
    )

    if st.button("Déchiffrer"):
        msg_propre = "".join(c for c in message_chiffre.upper() if c.isalpha())

        if not msg_propre:
            st.error("Entrez un message à déchiffrer.")
        else:
            dechiffre = destinataire.dechiffrer(message_chiffre)
            st.session_state.dernier_dechiffre = dechiffre
            st.success("Message déchiffré !")
            st.code(dechiffre)

    if st.session_state.dernier_dechiffre:
        st.markdown("### Dernier résultat")
        st.write(f"Texte déchiffré : `{st.session_state.dernier_dechiffre}`")


with tab3:
    st.header("Info")

    st.markdown(
        """
### Ce qu'il faut observer
- Si tu chiffres une première fois `BONJOUR`, tu obtiens un texte chiffré.
- Si tu déchiffres immédiatement ce message côté destinataire, tu dois retrouver `BONJOUR`.
- Si tu rechiffres ensuite `BONJOUR` **sans démarrer une nouvelle communication**, le résultat doit être différent.
- Si le destinataire déchiffre ensuite ce deuxième message dans le bon ordre, il retrouve encore `BONJOUR`.

### Point théorique important
- Le sujet n'interdit pas qu'une valeur apparaisse deux fois dans une clé.
- Ce qu'il interdit, c'est de **réutiliser le même flux de clé** pour deux messages.
- Donc il ne faut pas réinitialiser le paquet entre deux messages d'une même conversation.

### Dans cette application
- le paquet n'est pas recréé à chaque clic ;
- l'état du paquet est conservé dans `st.session_state` ;
- l'expéditeur et le destinataire progressent chacun de leur côté dans le même ordre.
"""
    )

    if st.button("Afficher l'état courant des paquets"):
        st.write("Paquet expéditeur (15 premières cartes) :", expediteur.paquet[:15])
        st.write("Paquet destinataire (15 premières cartes) :", destinataire.paquet[:15])