## CODE TEMPORAIRE EN ATTENDANT CELUI DE LITICIA
import random
from math import gcd

# Test de primalité simple (suffisant pour un exercice)
def is_prime(n, k=20):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2

    # Test de Fermat / Miller-Rabin simplifié
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

def generate_prime(bits=16):
    while True:
        n = random.getrandbits(bits)
        n |= 1  # force impair
        if is_prime(n):
            return n

def generate_keys():
    # deux nombres premiers p et q
    p = generate_prime(16)
    q = generate_prime(16)
    while q == p:
        q = generate_prime(16)

    n = p * q
    phi = (p - 1) * (q - 1)

    # e public : 65537 ou autre
    e = 65537
    # s'assurer que e et phi sont coprimes
    while gcd(e, phi) != 1:
        e += 2

    # calcul de d = inverse modulaire de e mod phi
    d = pow(e, -1, phi)

    # Retour au format attendu par ton script
    public = (n, e)
    private = (n, d)

    return public, private, p, q, phi
