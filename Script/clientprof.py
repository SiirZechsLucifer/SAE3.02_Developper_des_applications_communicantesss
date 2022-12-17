import socket

host1 = "localhost"
port1 = 7456


m_kill = "kill"
m_disconnect = "disconnect"
m_reset = "reset"

message = ""
print(f"Ouverture de la socket sur le serveur {host1} port {port1}")

client_socket = socket.socket()
client_socket.connect((host1, port1))

while message.lower() != m_kill and message.lower() != m_reset and message.lower() != m_disconnect:
    message = input(" -> ")
    if message != "":
        client_socket.send(message.encode())
        print(f"Message envoyé {message}")
        reponse = client_socket.recv(1024).decode("utf-8")
        print(f"Message reçu {reponse}")
        #print(f'{host1} > {reponse}')

# Fermeture de la socket du client
client_socket.close()
print("Socket fermée")
