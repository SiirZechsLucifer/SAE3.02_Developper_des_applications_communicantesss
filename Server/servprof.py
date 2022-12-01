import socket
import sys

m_kill = "kill"
m_disconnect = "disconnect"
m_reset = "reset"

host = "localhost"
port = 7456

message_client = ""

def execute_cmd(cmd):
    return str(cmd)

def serveur():
    message_client = ""
    while message_client != "kill":

        message_client = ""
        while message_client != "kill":
            server_socket = socket.socket()
            server_socket.bind((host, port))
            server_socket.listen(1)
            print(f"Socket ouverte sur {host} - {port}")

            message_client = ""
            while message_client != "kill" and message_client != "reset":
                print('FD> En attente du client')
                conn_client, address_client = server_socket.accept()
                print(f'Client connecté {address_client}')

                message_client = ""
                while message_client.lower() != m_kill and message_client.lower() != m_reset and message_client.lower() != m_disconnect:
                    message_client = conn_client.recv(1024).decode()
                    print(f"Message reçu {message_client}")
                    execution = execute_cmd(message_client)
                    conn_client.send(execution.encode())

                conn_client.close()
                print("Fermeture de la socket client")

            server_socket.close()
            print("Fermeture du serveur")


if __name__ == '__main__':
    serveur()