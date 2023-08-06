from . import utils
from . import interface as sc
import socket, json


class Client():
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.socket = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.socket.connect((self.IP, self.PORT))
        self.socket.settimeout(None)

    def send(self, data, key=None):
        data = json.dumps(data)
        sc.msg_send(self.socket, data)
    
    def recv(self, key=None):
        try:
            data = sc.msg_recv(self.socket)
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            utils.debug(data,"json Decode Error")
            return ""
        return data

    def close(self):
        if socket:
            self.socket.close()