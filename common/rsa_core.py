import random
from math import gcd

# -----------------------------
# Générer un nombre premier probable
# (équivalent de BigInteger.probablePrime)
# -----------------------------
def probable_prime(bits=2048):
    while True:
        n = random.getrandbits(bits)
        # forcer un nombre impair
        n |= 1
        if is_probable_prime(n):
            return n

# Test de primalité Miller-Rabin
def is_probable_prime(n, k=20):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # décomposition n-1 = d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x in (1, n - 1):
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

# -----------------------------
# Algorithme d’Euclide Étendu
# (équivalent algoEuclide du Java)
# -----------------------------
def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, u, v = extended_gcd(b, a % b)
    return (g, v, u - (a // b) * v)

# -----------------------------
# Génération des clés RSA
# -----------------------------
def generate_keys(bits=2048):
    # p et q grands entiers premiers
    p = probable_prime(bits)
    q = probable_prime(bits)
    while q == p:
        q = probable_prime(bits)

    # n = p * q
    n = p * q

    # m = (p - 1)*(q - 1)
    m = (p - 1) * (q - 1)

    # e nombre impair premier avec m
    # (équivalent du new BigInteger(512, new Random()) dans ton Java)
    while True:
        e = random.getrandbits(512)
        if e % 2 == 0:
            e -= 1
        if gcd(e, m) == 1:
            break

    # calcul de u (comme ton algoEuclide)
    g, u, v = extended_gcd(e, m)

    # on doit avoir u > 0
    u = u % m

    public_key = (n, e)
    private_key = (n, u)

    return public_key, private_key, p, q, m
