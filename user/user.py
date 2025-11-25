# user.py
# Client/serveur simple: échange de clé publique puis échange de messages chiffrés.
# Usage: lancer ce script sur deux machines (ou deux terminaux) ; chacun essaie de se connecter à l'autre.
# Si la connexion échoue, le script écoute (mode serveur). Une fois connecté : échange de clé publique, puis envoi/recep.

import socket
import threading
import json
import sys
import os

from keys import load_key, create_keys_file
from crypto import encrypt_message, decrypt_message, serialize_cipher, parse_cipher
import utilsnetwork as net

# ----- Config -----
DEFAULT_HOST = '192.168.10.125'  # modifie si nécessaire
PORT = 12345
KEYS_DIR = "."  # répertoire actuel

PUBLIC_KEY_FILE = os.path.join(KEYS_DIR, "public.key")
PRIVATE_KEY_FILE = os.path.join(KEYS_DIR, "private.key")
OTHER_PUBLIC_FILE = os.path.join(KEYS_DIR, "other_public.key")

# ----- Chargement/génération des clés locales -----
def ensure_keys(bits=32):
    # crée des clés si elles n'existent pas
    if not os.path.exists(PUBLIC_KEY_FILE) or not os.path.exists(PRIVATE_KEY_FILE):
        print("Clés locales absentes : génération (taille demo: {} bits)".format(bits))
        create_keys_file(bits=bits, public_path=PUBLIC_KEY_FILE, private_path=PRIVATE_KEY_FILE)
    pub = load_key(PUBLIC_KEY_FILE)
    priv = load_key(PRIVATE_KEY_FILE)
    # format (n, e) et (n, d)
    public = (pub['n'], pub['e'])
    private = (priv['n'], priv.get('d') or priv.get('u'))  # accepte 'd' ou 'u'
    return public, private

# ----- Envoi de clé publique -----
def send_pubkey(sock, public):
    n, e = public
    msg = json.dumps({"type": "PUBKEY", "n": n, "e": e}).encode()
    net.send_msg(sock, msg)

def parse_pubkey(json_bytes):
    obj = json.loads(json_bytes)
    if obj.get("type") != "PUBKEY":
        raise ValueError("Attendu PUBKEY")
    return (int(obj['n']), int(obj['e']))

# ----- Thread de réception -----
def handle_receive(sock, private_key, peer_public_container):
    try:
        while True:
            data = net.recv_msg(sock)
            obj = json.loads(data)
            typ = obj.get("type")
            if typ == "PUBKEY":
                peer_public_container['key'] = (int(obj['n']), int(obj['e']))
                print("Clé publique du pair reçue :", peer_public_container['key'])
            elif typ == "CIPHER":
                cipher = obj.get("data")
                plaintext = decrypt_message(cipher, private_key)
                print("\n--- Message reçu (déchiffré) ---")
                print(plaintext)
                print("--------------------------------")
                # Si on veut répondre automatiquement (BOB) : ici on ne répond pas automatiquement
            else:
                print("Message inconnu reçu :", obj)
    except Exception as e:
        print("Erreur réception :", e)

# ----- Boucle principale -----
def main():
    public, private = ensure_keys(bits=32)
    peer_public = {'key': None}
    host = DEFAULT_HOST
    port = PORT

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.0)
    try:
        s.connect((host, port))
        s.settimeout(None)
        print("Connecté en tant que client à", (host, port))
        role = "ALICE"
    except Exception:
        # passe en mode serveur
        s.close()
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind(("0.0.0.0", port))
        srv.listen(1)
        print("En attente d'une connexion sur le port", port)
        conn, addr = srv.accept()
        s = conn
        print("Connexion acceptée de", addr)
        role = "BOB"

    # envoyer la clé publique
    send_pubkey(s, public)

    # démarrer le thread récepteur
    recv_thread = threading.Thread(target=handle_receive, args=(s, private, peer_public), daemon=True)
    recv_thread.start()

    # boucle d'envoi
    try:
        while True:
            msg = input("Message à envoyer (ou 'quit' pour sortir) : ")
            if msg.lower() in ("quit", "exit"):
                print("Fermeture.")
                s.close()
                break
            if peer_public['key'] is None:
                print("Attente de la clé publique du pair...")
                continue
            cipher = encrypt_message(msg, peer_public['key'])
            # envoyer en JSON
            payload = json.dumps({"type":"CIPHER", "data": cipher}).encode()
            net.send_msg(s, payload)
            print("Message chiffré envoyé.")
    except KeyboardInterrupt:
        print("Interrompu par l'utilisateur.")
        s.close()

if __name__ == "__main__":
    main()
