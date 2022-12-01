import socket

host = "localhost"
port = 7456

m_kill = "kill"
m_disconnect = "disconnect"
m_reset = "reset"

message = ""
print(f"Ouverture de la socket sur le serveur {host} port {port}")

client_socket = socket.socket()
client_socket.connect((host, port))

while message.lower() != m_kill and message.lower() != m_reset and message.lower() != m_disconnect:
    message = input(" -> ")
    client_socket.send(message.encode())
    print("Message envoyé")
    reponse = client_socket.recv(10000).decode()
    print(f'{host} > {reponse}')

# Fermeture de la socket du client
client_socket.close()
print("Socket fermée")
