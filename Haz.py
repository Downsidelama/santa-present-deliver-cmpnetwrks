import sys
import socket

import Terkep


class SimpleDgramServer:

    def __init__(self, name):
        haz = Terkep.Hazak().get_haz(haz_name=name)
        self.csomagok = list()
        if haz is not None:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_address = ('localhost', haz)
            self.server.bind(self.server_address)
            print("A haz szerver online!")
        else:
            print("Nincs ilyen nevu haz!")
            sys.exit(1)

    def run_server(self):
        while True:
            data, client_address = self.server.recvfrom(4096)
            if "csomag" in data.decode():
                self.csomagok.append(data.decode)
                print("kaptam egy csomagot!")
                self.server.sendto("OK".encode(), client_address)


haz_id = input("Kerem a haz nevet: ")
server = SimpleDgramServer(haz_id)
server.run_server()
