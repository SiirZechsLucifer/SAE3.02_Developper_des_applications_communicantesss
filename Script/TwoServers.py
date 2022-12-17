
import socket

host1 = "localhost"
port1 = 7456

host2 = "localhost"
port2 = 7457


m_kill = "kill"
m_disconnect = "disconnect"
m_reset = "reset"

message = ""
# Deffinition d'une liste de connexion
client_socket = []

client_socket.append(socket.socket())
client_socket[0].connect((host1, port1))

client_socket.append(socket.socket())
client_socket[1].connect((host2, port2))

while message.lower() != m_kill and message.lower() != m_reset and message.lower() != m_disconnect:
    message = input(" -> ")
    if message != "":
        for client_sock in client_socket:
            client_sock.send(message.encode())
            print(f"Message envoyé {message}")
            reponse = client_sock.recv(1024).decode()
            print(f"Message reçu: {reponse}")

# Fermeture de la socket du client
client_socket.close()
print("Socket fermée")
