import tkinter as tk
from tkinter import messagebox
from deck import Deck
from solitaire import encrypt, decrypt

suit_symbols = {"C": "♣️", "D": "♦️", "H": "♥️", "S": "♠️"}

class SolitaireApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Mini-projet – Algorithme Solitaire")
        self.root.geometry("1700x800")

        # Deux paquets indépendants
        self.deck_sender = Deck()
        self.deck_receiver = Deck()

        self.last_key_sender = None

        self.auto_key_var = tk.IntVar()

        self.create_layout()

    # ===================== LAYOUT =====================
    def create_layout(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ================= SENDER =================
        self.left_frame = tk.Frame(main_frame, bd=2, relief="groove", padx=10, pady=10)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(self.left_frame, text="🔐 Sender A - Chiffrement", font=("Arial", 16)).pack(pady=5)

        tk.Checkbutton(
            self.left_frame,
            text="Clé aléatoire automatique",
            variable=self.auto_key_var
        ).pack(pady=5)

        tk.Label(self.left_frame, text="Message original").pack()
        self.message_entry = tk.Entry(self.left_frame, width=45)
        self.message_entry.pack(pady=5)

        tk.Button(self.left_frame, text="Chiffrer", command=self.encrypt_message, bg="lightgreen").pack(pady=5)
        tk.Button(self.left_frame, text="Nouvelle clé manuelle", command=lambda: self.shuffle_deck("sender"), bg="orange").pack(pady=5)

        tk.Label(self.left_frame, text="Message chiffré").pack()
        self.cipher_entry = tk.Entry(self.left_frame, width=45)
        self.cipher_entry.pack(pady=5)

        tk.Label(self.left_frame, text="Paquet Sender").pack(pady=5)
        self.deck_frame_sender = tk.Frame(self.left_frame)
        self.deck_frame_sender.pack()

        tk.Label(self.left_frame, text="Processus de chiffrement").pack(pady=5)
        self.log_sender = tk.Text(self.left_frame, height=12, width=60, state="disabled", bg="#f2f2f2")
        self.log_sender.pack()

        self.update_deck_display("sender")

        # ================= RECEIVER =================
        self.right_frame = tk.Frame(main_frame, bd=2, relief="groove", padx=10, pady=10)
        self.right_frame.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(self.right_frame, text="🔓 Receiver B - Déchiffrement", font=("Arial", 16)).pack(pady=5)

        tk.Label(self.right_frame, text="Message chiffré reçu").pack()
        self.cipher_entry_dec = tk.Entry(self.right_frame, width=45)
        self.cipher_entry_dec.pack(pady=5)

        tk.Button(self.right_frame, text="Déchiffrer", command=self.decrypt_message, bg="lightblue").pack(pady=5)
        tk.Button(self.right_frame, text="Nouvelle clé manuelle", command=lambda: self.shuffle_deck("receiver"), bg="orange").pack(pady=5)

        tk.Label(self.right_frame, text="Message déchiffré").pack()
        self.plain_entry = tk.Entry(self.right_frame, width=45)
        self.plain_entry.pack(pady=5)

        tk.Label(self.right_frame, text="Paquet Receiver").pack(pady=5)
        self.deck_frame_receiver = tk.Frame(self.right_frame)
        self.deck_frame_receiver.pack()

        tk.Label(self.right_frame, text="Processus de déchiffrement").pack(pady=5)
        self.log_receiver = tk.Text(self.right_frame, height=12, width=60, state="disabled", bg="#f2f2f2")
        self.log_receiver.pack()

        self.update_deck_display("receiver")

    # ===================== LOG =====================
    def log(self, text, side):
        log_widget = self.log_sender if side == "sender" else self.log_receiver
        log_widget.config(state="normal")
        log_widget.insert(tk.END, text + "\n")
        log_widget.see(tk.END)
        log_widget.config(state="disabled")

    # ===================== DECK DISPLAY =====================
    def update_deck_display(self, side):
        frame = self.deck_frame_sender if side == "sender" else self.deck_frame_receiver
        deck = self.deck_sender if side == "sender" else self.deck_receiver

        for widget in frame.winfo_children():
            widget.destroy()

        cards = deck.display()

        for i, card in enumerate(cards):
            text = card
            color = "black"

            if "JOKER_A" in card:
                text = "🃏"
            elif "JOKER_B" in card:
                text = "🃏"
                color = "red"
            elif len(card) >= 2 and card[1] in suit_symbols:
                text = f"{card[0]}{suit_symbols[card[1]]}"
                if card[1] in ["H", "D"]:
                    color = "red"

            tk.Label(
                frame,
                text=text,
                borderwidth=1,
                relief="solid",
                width=4,
                fg=color,
                font=("Arial", 13)
            ).grid(row=i // 13, column=i % 13, padx=2, pady=2)

    # ===================== SHUFFLE =====================
    def shuffle_deck(self, side):
        deck = self.deck_sender if side == "sender" else self.deck_receiver
        deck.shuffle()
        self.update_deck_display(side)

    # ===================== ENCRYPT =====================
    def encrypt_message(self):
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Erreur", "Pas de message à chiffrer")
            return

        self.log_sender.config(state="normal")
        self.log_sender.delete(1.0, tk.END)
        self.log_sender.config(state="disabled")

        self.log("=== CHIFFREMENT ===", "sender")
        self.log(f"Message original : {message}", "sender")

        cipher, key, steps = encrypt(message, self.deck_sender)

        self.cipher_entry.delete(0, tk.END)
        self.cipher_entry.insert(0, cipher)

        # Envoi automatique au receiver
        self.cipher_entry_dec.delete(0, tk.END)
        self.cipher_entry_dec.insert(0, cipher)

        self.last_key_sender = key

        for step in steps:
            self.log(step, "sender")

        self.log(f"Résultat final : {cipher}", "sender")

        # Auto clé côté sender uniquement
        if self.auto_key_var.get():
            self.shuffle_deck("sender")

    # ===================== DECRYPT =====================
    def decrypt_message(self):
        cipher = self.cipher_entry_dec.get()

        if not cipher or not self.last_key_sender:
            messagebox.showerror("Erreur", "Aucun message ou clé disponible")
            return

        self.log_receiver.config(state="normal")
        self.log_receiver.delete(1.0, tk.END)
        self.log_receiver.config(state="disabled")

        self.log("=== DECHIFFREMENT ===", "receiver")
        self.log(f"Message reçu : {cipher}", "receiver")

        plain, steps = decrypt(cipher, self.deck_receiver, self.last_key_sender)

        self.plain_entry.delete(0, tk.END)
        self.plain_entry.insert(0, plain)

        for step in steps:
            self.log(step, "receiver")

        self.log(f"Message original retrouvé : {plain}", "receiver")

        # Auto clé côté receiver uniquement après déchiffrement
        if self.auto_key_var.get():
            self.shuffle_deck("receiver")


if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireApp(root)
    root.mainloop()