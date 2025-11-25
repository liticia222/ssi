# rsa_core.py
# Cœur RSA : génération de clés, algorithme d'Euclide étendu, chiffrement/déchiffrement d'entiers.

import random
from math import gcd

# --- Miller-Rabin pour test de primalité ---
def is_probable_prime(n, k=10):
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # write n-1 as d*2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=32):
    """Génère un nombre premier probable de 'bits' bits (pour démo)."""
    assert bits >= 8
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1)) | 1  # s'assure que le bit de poids fort et impair sont à 1
        if is_probable_prime(n):
            return n

# --- Euclide étendu (Bézout) ---
def extended_gcd(a, b):
    """Retourne (g, x, y) tel que a*x + b*y = g = gcd(a, b)."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t

def modinv(e, phi):
    """Inverse modulaire de e modulo phi en utilisant Euclide étendu.
       Retourne d tel que (d*e) % phi == 1 ou lève ValueError si pas d'inverse."""
    g, x, _ = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Pas d'inverse modulaire : e et phi ne sont pas premiers entre eux.")
    return x % phi

# --- Génération de clés ---
def generate_keys(bits=32, choose_e=65537):
    """Génère (public, private, p, q, phi).
       bits correspond à la taille de p et q chacun (taille pour démo)."""
    # Génération de p et q distincts
    p = generate_prime(bits)
    q = generate_prime(bits)
    while q == p:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choisir e : on peut utiliser un e par défaut (65537) ou rechercher un e premier avec phi
    e = choose_e
    # si e n'est pas coprime avec phi, on cherche un autre e impair
    while gcd(e, phi) != 1:
        e += 2

    # Calcul de d (inverse modulaire)
    d = modinv(e, phi)

    public = (n, e)
    private = (n, d)
    return public, private, p, q, phi

# --- Opérations sur entiers (utilisées par crypto.py) ---
def encrypt_int(m_int, public_key):
    n, e = public_key
    return pow(m_int, e, n)

def decrypt_int(c_int, private_key):
    n, d = private_key
    return pow(c_int, d, n)

# Si on veut utiliser la classe, on peut aussi exposer ces fonctions :
__all__ = [
    "is_probable_prime", "generate_prime",
    "extended_gcd", "modinv",
    "generate_keys", "encrypt_int", "decrypt_int"
]
