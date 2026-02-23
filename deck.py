# deck.py

import random

class Deck:
    def __init__(self):
        self.reset()

    # =========================
    # Création du paquet
    # =========================
    def reset(self):
        suits = ["C", "D", "H", "S"]
        ranks = [str(i) for i in range(1, 14)]

        self.cards = [r + s for s in suits for r in ranks]

        # Deux jokers
        self.cards.append("JOKER_A")
        self.cards.append("JOKER_B")

    # =========================
    # Mélange du paquet
    # =========================
    def shuffle(self):
        random.shuffle(self.cards)

    # =========================
    # Affichage
    # =========================
    def display(self):
        return self.cards

    # =========================
    # Génération flux de clé
    # =========================
    def generate_keystream(self, length):
        """
        Version simplifiée :
        Utilise la position des cartes pour générer
        des nombres entre 1 et 26
        """

        keystream = []

        for i in range(length):
            # On prend la carte du dessus
            top_card = self.cards[i % len(self.cards)]

            # Transformer carte en valeur numérique
            if "JOKER" in top_card:
                value = random.randint(1, 26)
            else:
                rank = int(top_card[:-1])
                value = rank % 26
                if value == 0:
                    value = 26

            keystream.append(value)

        return keystream