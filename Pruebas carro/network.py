import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ttl = struct.pack('b', 1)
        self.client.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)   
        self.addr = ('224.3.29.71', 5000)

        self.id = self.connect()

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
