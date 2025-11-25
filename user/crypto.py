# crypto.py
# Encodage texte -> liste d'entiers, chiffrement/déchiffrement de messages
# Utilise rsa_core.encrypt_int/decrypt_int

import json
from rsa_core import encrypt_int, decrypt_int

# --- encodage simple : ASCII ord pour chaque caractère ---
def encode_text_ascii(text):
    """Transforme une chaîne en liste d'entiers (ASCII)."""
    return [ord(c) for c in text]

def decode_text_ascii(int_list):
    """Transforme une liste d'entiers en texte (chr)."""
    return ''.join(chr(i) for i in int_list)

# --- chiffrement/déchiffrement d'un message texte complet ---
def encrypt_message(text, public_key):
    """Retourne une liste d'entiers chiffrés (prête à être sérialisée)."""
    encoded = encode_text_ascii(text)
    cipher = [encrypt_int(m, public_key) for m in encoded]
    return cipher

def decrypt_message(cipher_list, private_key):
    """Prend une liste d'entiers chiffrés, retourne le texte en clair."""
    decoded = [decrypt_int(c, private_key) for c in cipher_list]
    return decode_text_ascii(decoded)

# --- fonctions utilitaires pour sérialisation JSON ---
def serialize_cipher(cipher_list):
    # JSON simple : liste d'entiers
    return json.dumps({"type":"CIPHER","data": cipher_list})

def parse_cipher(json_bytes):
    obj = json.loads(json_bytes)
    if obj.get("type") != "CIPHER":
        raise ValueError("Mauvais type de message")
    return obj["data"]
