from PyQt5.QtWidgets import QWidget, QTabWidget, QGridLayout, QLabel, QTextEdit, QLineEdit, QPushButton, QApplication, \
    QMainWindow
import sys
import threading
import socket


class client_window(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QGridLayout()
        widget.setLayout(layout)

        self.__host_line_edit = QLineEdit()
        self.__host_line_edit.setPlaceholderText("Insérez l'adresse")

        self.__port_line_edit = QLineEdit()
        self.__port_line_edit.setPlaceholderText('Insérez le PORT')

        self.__connect_button = QPushButton('Connection')
        self.__connect_button.clicked.connect(self.__connection)
        self.__ecriremsg = QLineEdit()
        self.__ecriremsg.setPlaceholderText('ECRIRE COMMANDE')
        self.__ecriremsg.returnPressed.connect(self.__sendmsg)
        self.__envoimsg = QPushButton('ENVOI')
        self.__envoimsg.clicked.connect(self.__sendmsg)

        self.__terminal = QTextEdit()
        self.__terminal.setReadOnly(True)

        layout.addWidget(self.__host_line_edit, 0, 0)
        layout.addWidget(self.__port_line_edit, 0, 1)
        layout.addWidget(self.__connect_button, 0, 2)
        layout.addWidget(self.__terminal, 1, 0, 1, 3)
        layout.addWidget(self.__ecriremsg, 2, 0, 1, 2)
        layout.addWidget(self.__envoimsg, 2, 2, 1, 1)

        self.__client_socket = None
        self.__arret = False

    def __connection(self):
        address = self.__host_line_edit.text()
        port = self.__port_line_edit.text()
        if port.isdigit():
            if self.__client_socket is None:
                port = int(port)
                self.__client_socket = socket.socket()
                try:
                    self.__client_socket.connect((address, port))
                    self.__client_socket.setblocking(False)
                    threading.Thread(target=self.__ecoute).start()
                except:
                    self.__client_socket = None
                    print('connection impossible')
        else:
            print('INSERER UN NOMBRE')

    def __ecoute(self):
        while not self.__arret:
            try:
                data = self.__client_socket.recv(1024).decode()
                if data is not None:
                    if len(data) > 0:
                        self.__terminal.setText(self.__terminal.text() + data + '\n')
            except:
                pass

    def __sendmsg(self):
        commande = self.__ecriremsg.text()
        if len(commande) > 0:
            self.__ecriremsg.setText('')
            try:
                self.__client_socket.send(commande.encode())
            except:
                self.__terminal.setText(self.__terminal.text() + 'Connection perdue\n')

    def closeEvent(self, event):
        self.__client_socket.close()
        self.__arret = True
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = client_window()
    window.show()
    app.exec()
