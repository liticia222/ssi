import socket
import threading
from rsa_core import generate_keys, pow  # pow est pour le chiffrement simple

# Génération clés
public, private, p, q, phi = generate_keys()
n, e = public
n2, d = private

peer_public_key = None
role = None
last_message_sent = None

def encrypt(message, key):
    n, e = key
    return [pow(ord(c), e, n) for c in message]

def decrypt(cipher, key):
    n, d = key
    return ''.join([chr(pow(c, d, n)) for c in cipher])

def handle_receive(sock):
    global role, peer_public_key
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            # réception de la clé publique
            if data.startswith(b'PUBKEY:'):
                n_peer, e_peer = map(int, data[7:].decode().split(','))
                peer_public_key = (n_peer, e_peer)
                print(f"Clé publique reçue : {peer_public_key}")
            else:
                cipher = eval(data.decode())
                plaintext = decrypt(cipher, private)
                print(f"\nMessage reçu : {plaintext}")

                if role is None:
                    role = "BOB"
                    print("Je suis Bob")

                if role == "BOB":
                    # réponse : chiffrement avec clé publique de l'autre
                    cipher_response = encrypt(plaintext, peer_public_key)
                    sock.send(str(cipher_response).encode())
        except Exception as e:
            print("Erreur :", e)
            break

def main():
    global role, peer_public_key, last_message_sent

    host = '192.168.116.125'  # IP de l'autre machine
    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print("Connecté en tant que client")
        role = "ALICE"
    except:
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print("En attente d'une connexion...")
        s, addr = s.accept()
        print(f"Connexion établie avec {addr}")
        role = None  # rôle sera déterminé plus tard

    # envoi de la clé publique
    s.send(f"PUBKEY:{n},{e}".encode())

    # thread pour recevoir les messages
    threading.Thread(target=handle_receive, args=(s,), daemon=True).start()

    # boucle pour envoyer des messages
    while True:
        msg = input("Message à envoyer : ")
        if peer_public_key is None:
            print("Attente de la clé publique du pair...")
            continue
        cipher_msg = encrypt(msg, peer_public_key)
        last_message_sent = msg
        s.send(str(cipher_msg).encode())
        if role is None:
            role = "ALICE"
            print("Je suis Alice")

if __name__ == "__main__":
    main()
