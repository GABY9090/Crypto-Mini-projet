# Crypto-Mini-projet

Ce projet est une **implémentation avec interface graphique Tkinter** du chiffrement Solitaire Cipher (ou projet éducatif basé sur les cartes).  
Actuellement, le chiffrement/déchiffrement peut être désactivé pour ne garder que l’interface.

---

## Structure des fichiers

### 1. `deck.py`
- Contient la classe `Deck` qui représente un paquet de cartes.
- Fonctions principales :
  - `reset()` → crée un paquet de 52 cartes + 2 jokers.
  - `display()` → retourne le paquet pour affichage.
- Si le chiffrement n’est pas utilisé, c’est suffisant pour l’interface.

### 2. `interface.py`
- Contient la classe `SolitaireApp` qui gère **l’interface Tkinter**.
- Affiche les deux paquets de cartes (Sender et Receiver), les boutons et les logs.
- Les boutons “Chiffrer” et “Déchiffrer” peuvent être désactivés si on ne fait plus de chiffrement.
- Met à jour dynamiquement l’affichage des cartes.

### 3. `solitaire.py`
- Contient le code de chiffrement et déchiffrement **via l’algorithme Solitaire Cipher**.
- Fonctionnalités :
  - Nettoyage du texte (`clean_text`)
  - Conversion texte ↔ nombres
  - Chiffrement (`encrypt`) et déchiffrement (`decrypt`)
- Peut être supprimé si on ne souhaite garder que l’interface.

### 4. `main.py`
- Point d’entrée pour lancer le projet.
- Crée la fenêtre Tkinter et initialise `SolitaireApp`.
- Commande pour lancer :  
```bash
python main.py
