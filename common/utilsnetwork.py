# utilsnetwork.py
# Fonctions d'envoi/réception avec framing (4-byte length prefix)

import struct
import socket

def send_msg(sock: socket.socket, data: bytes):
    """Envoie data précédé d'une longueur 4-octets big-endian."""
    length = struct.pack('>I', len(data))
    sock.sendall(length + data)

def recv_all(sock: socket.socket, n: int):
    """Reçoit exactement n octets (ou lève exception si EOF)."""
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socket closed pendant la réception")
        data += chunk
    return data

def recv_msg(sock: socket.socket):
    """Reçoit un message encodé with 4-byte length prefix. Retourne bytes du payload."""
    raw_len = recv_all(sock, 4)
    (length,) = struct.unpack('>I', raw_len)
    return recv_all(sock, length)
