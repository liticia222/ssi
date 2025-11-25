# keys.py
# Génération, sauvegarde et chargement de clés (format simple clé=valeur par ligne)

import os
from rsa_core import generate_keys

def save_key(path, data: dict):
    with open(path, "w") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")

def load_key(path):
    """Charge une clé à partir d'un fichier 'k=v' par ligne. Retourne dict."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} introuvable")
    data = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            k, v = line.split('=', 1)
            data[k] = int(v)
    return data

def create_keys_file(bits=32, public_path="public.key", private_path="private.key"):
    pub, priv, p, q, phi = generate_keys(bits=bits)
    n, e = pub
    n2, d = priv
    save_key(public_path, {"n": n, "e": e})
    save_key(private_path, {"n": n2, "d": d})
    print("Clés générées :")
    print("p =", p)
    print("q =", q)
    print("n =", n)
    print("phi =", phi)
    print("e =", e)
    print("d =", d)

if __name__ == "__main__":
    create_keys_file(bits=32)
