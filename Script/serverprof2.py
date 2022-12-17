import socket
import platform
import psutil
import subprocess
import sys

m_kill = "kill"
m_disconnect = "disconnect"
m_reset = "reset"

defaut_host = "localhost"
defaut_port = 7457

message_client = ""


def name():
    hostname = socket.gethostname()
    return f"{hostname}"


def os():
    os = platform.platform()
    return f"{os}"


def cpu():
    cpu = platform.processor()
    return f"{cpu}"

def ram():
    ram = psutil.virtual_memory()[2]
    memd = psutil.virtual_memory()[0]/1000000000
    memu = psutil.virtual_memory()[3]/1000000000
    meml = psutil.virtual_memory()[4]/1000000000
    return f"la mémoire total du système est de {memd} Go, la mémoire utilisé est de {memu} Go, son pourcentage est de {ram}%, l'espace mémoire libre est de {meml} Go "


def ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return IPAddr


def execute_cmd(cmd):
    if cmd == "NAME":
        rep = name()
        print(rep)
        # return rep
    elif cmd == "OS":
        rep = os()
        print(rep)
        # return rep

    elif cmd == "CPU":
        rep = cpu()
        print(rep)
        # return rep

    elif cmd == "RAM":
        rep = ram()
        print(f"{rep}%")

    elif cmd == "IP":
        rep = ip()
        print(f"{rep}")

    elif cmd[0:4] == "DOS:":
        x = cmd.split(":")[1]
        output = str(subprocess.check_output(x,shell=True).decode("cp850"))
        return f"{output}"

    elif cmd[0:4] == "ping":
        x = cmd.split(" ")[1]
        output = subprocess.getoutput(cmd)
        return f"{output}"

    else:
        rep = f"Unknown commande {cmd}"

    return rep


def serveur(host, port):
    #mon_nom = name()
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
                    #execution = f'{mon_nom} > {execution}'
                    #execution = f'{execution}'
                    conn_client.send(execution.encode())

                conn_client.close()
                print("Fermeture de la socket client")

            server_socket.close()
            print("Fermeture du serveur")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(sys.argv[1])
        serveur(defaut_host, int(sys.argv[1]))
    else:
        serveur(defaut_host, defaut_port)
