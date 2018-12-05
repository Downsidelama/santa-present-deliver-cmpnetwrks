import socket
import sys
import struct
from time import sleep

import Terkep


class SimpleTCPSelectClient:
    def __init__(self, server_addr='localhost', server_port=10001):
        self.setup_client(server_addr, server_port)
        self.struktura = struct.Struct('10s 5s')
        self.hazak = dict()
        self.dgram_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def setup_client(self, server_addr, server_port):
        server_address = (server_addr, server_port)

        # Create a TCP/IP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.client.connect(server_address)

    def handle_incoming_message_from_remote_server(self):
        data = self.client.recv(1)
        if not data:
            print('\nDisconnected from server')
            sys.exit()
        else:
            csom_num = int(data.decode())
            for i in range(csom_num):
                data = self.client.recv(15)
                data = self.struktura.unpack(data)
                print(data[0].decode(), data[1].decode())
                self.deliver_to_house(data)

    def deliver_to_house(self, data):
        haz_nev = data[1].decode().strip('\x00')
        csomag_nev = data[0].decode().strip('\x00')
        if haz_nev in self.hazak:
            self.send_udp(csomag_nev, haz_nev)
        else:
            haz_nev = haz_nev
            haz_port = Terkep.Hazak().get_haz(haz_nev)
            if haz_port is not None:
                self.hazak[haz_nev] = ('localhost', haz_port)
                self.send_udp(csomag_nev, haz_nev)
            else:
                print("Nincs ilyen haz!")

    def send_udp(self, csomag_nev, haz_nev):
        try:
            self.dgram_server.sendto(csomag_nev.encode(), self.hazak[haz_nev])
            data, addr = self.dgram_server.recvfrom(4096)
            if data.decode().strip() == "OK":
                print("A csomag sikeresen leszallitva a hazhoz.")
            else:
                print("Hiba tortent a csomag kiszallitasa soran (nem vart valasz).")
        except ConnectionResetError:
            print('Csatlakozas a hazhoz meghiusult.')

    def handle_connection(self):
        while True:
            msg = 'request package'
            msg = msg.strip()
            self.client.send(msg.encode())
            print('requesting packages from the warehouse')
            self.handle_incoming_message_from_remote_server()
            sleep(5)


simpleTCPSelectClient = SimpleTCPSelectClient()
simpleTCPSelectClient.handle_connection()
