import socket


def server():
    host = 'localhost'
    port = 802

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1)
    conn_client, client_address = server_socket.accept()
    print("Server started ... connexion via {}".format(client_address))

    while True:
        data = conn_client.recv(1024).decode()
        if data == 'reset':
            print('restarting')
            conn_client.close()
            server_socket.listen(1)
            conn_client, client_address = server_socket.accept()
            break
        print(f"from connected user{host}:" + str(data))
        data = input(' -> ')
        conn_client.send(data.encode())
    conn_client.close()




if __name__ == '__main__':
    server()
