import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 12345))
print("Connecte to server")

client_socket.send("Hello from the client".encode())

reponse = client_socket.recv(1024).decode()
print(f"Received reponse : {reponse}")

client_socket.close()

