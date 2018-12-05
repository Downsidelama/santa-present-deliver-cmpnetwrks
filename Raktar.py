import select
import socket
import sys
import struct
import random


class SimpleTCPSelectServer:
    def __init__(self, addr='localhost', port=10001, timeout=1):
        self.server = self.setupServer(addr, port)
        # Sockets from which we expect to read
        self.inputs = [self.server]
        # Wait for at least one of the sockets to be ready for processing
        self.timeout = timeout
        self.structure = struct.Struct('10s 5s')
        self.csomag_num = 0

    def setupServer(self, addr, port):
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = (addr, port)
        server.bind(server_address)

        # Listen for incoming connections
        server.listen(5)
        return server

    def handleNewConnection(self, sock):
        # A "readable" server socket is ready to accept a connection
        connection, client_address = sock.accept()
        connection.setblocking(0)  # or connection.settimeout(1.0)
        self.inputs.append(connection)

    def handleDataFromClient(self, sock):
        try:
            data = sock.recv(1024)
            data = data.strip()
            if data and data.decode().strip() == 'request package':
                csom_num_rand = random.randrange(1, 4)
                sock.sendall(str(csom_num_rand).encode())
                print("sending %d presents" % csom_num_rand)
                for i in range(csom_num_rand):
                    csom_rnd = random.randrange(1, 101)
                    haz_rnd = random.randrange(1, 4)
                    send_data = (('csomag%d' % csom_rnd).encode(), ('haz%d' % haz_rnd).encode())
                    sock.sendall(self.structure.pack(*send_data))
            else:
                # Interpret empty result as closed connection
                print(sys.stderr, 'closing', sock.getpeername(), 'after reading no data')
                # Stop listening for input on the connection
                self.inputs.remove(sock)
                sock.close()
        except ConnectionResetError:
            print('a santa disconnected forcefully')
            self.inputs.remove(sock)

    def handleInputs(self, readable):
        for sock in readable:
            if sock is self.server:
                self.handleNewConnection(sock)
            else:
                self.handleDataFromClient(sock)

    def handleExceptionalCondition(self, exceptional):
        for sock in exceptional:
            print(sys.stderr, 'handling exceptional condition for', sock.getpeername())
            # Stop listening for input on the connection
            self.inputs.remove(sock)
            sock.close()

    def handleConnections(self):
        while self.inputs:
            try:
                readable, writable, exceptional = select.select(self.inputs, [], self.inputs, self.timeout)

                if not (readable or writable or exceptional):
                    # print >>sys.stderr, '  timed out, do some other work here'
                    continue

                self.handleInputs(readable)
                self.handleExceptionalCondition(exceptional)
            except KeyboardInterrupt:
                print("Close the system")
                for c in self.inputs:
                    c.close()
                self.inputs = []


simpleTCPSelectServer = SimpleTCPSelectServer()
simpleTCPSelectServer.handleConnections()
