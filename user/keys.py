import sys
import os

# ajoute le dossier "../common" au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(current_dir, "..", "common")
sys.path.append(common_dir)

from rsa_core import generate_keys

def save_key(path, data):
    with open(path, "w") as f:
        for k, v in data.items():
            f.write(f"{k}={v}\n")

def create_keys():
    public, private, p, q, m = generate_keys()

    n, e = public
    n2, u = private

    # clé publique
    save_key("public.key", {"n": n, "e": e})

    # clé privée
    save_key("private.key", {"n": n2, "u": u})

    print("Clés Alice générées avec succès !")
    print("p =", p)
    print("q =", q)
    print("n =", n)
    print("m =", m)
    print("e =", e)
    print("u =", u)

if __name__ == "__main__":
    create_keys()
