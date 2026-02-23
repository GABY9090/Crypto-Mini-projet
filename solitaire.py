# solitaire.py

import string

alphabet = string.ascii_uppercase


# =========================
# Nettoyage du texte
# =========================
def clean_text(text):
    return ''.join([c for c in text.upper() if c in alphabet])


# =========================
# Conversion texte ↔ nombres
# =========================
def text_to_numbers(text):
    return [ord(c) - 64 for c in text]


def numbers_to_text(numbers):
    return ''.join([chr(n + 64) for n in numbers])


# =========================
# CHIFFREMENT
# =========================
def encrypt(message, deck):
    message = clean_text(message)
    steps = []

    msg_nums = text_to_numbers(message)
    steps.append(f"Message nettoyé : {message}")
    steps.append(f"Valeurs numériques : {msg_nums}")

    # Génération flux depuis le deck
    key_stream = deck.generate_keystream(len(msg_nums))
    steps.append(f"Flux de clé généré : {key_stream}")

    encrypted_nums = []
    key_values = []

    for m, k in zip(msg_nums, key_stream):
        value = m + k
        if value > 26:
            value -= 26

        encrypted_nums.append(value)
        key_values.append(k)

        steps.append(f"{m} + {k} = {value}")

    cipher = numbers_to_text(encrypted_nums)
    steps.append(f"Message chiffré final : {cipher}")

    return cipher, key_values, steps


# =========================
# DECHIFFREMENT
# =========================
def decrypt(cipher, deck, key_values):
    cipher = clean_text(cipher)
    steps = []

    cipher_nums = text_to_numbers(cipher)
    steps.append(f"Message chiffré nettoyé : {cipher}")
    steps.append(f"Valeurs numériques : {cipher_nums}")
    steps.append(f"Clé utilisée : {key_values}")

    decrypted_nums = []

    for c, k in zip(cipher_nums, key_values):
        value = c - k
        if value <= 0:
            value += 26

        decrypted_nums.append(value)

        steps.append(f"{c} - {k} = {value}")

    plain = numbers_to_text(decrypted_nums)
    steps.append(f"Message original retrouvé : {plain}")

    return plain, steps