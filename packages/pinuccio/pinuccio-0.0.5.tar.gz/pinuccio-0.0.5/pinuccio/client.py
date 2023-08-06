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
        self.socket.connect((self.IP, self.PORT))

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
    
    def subscribe(self, name=""):
        if self.socket:
            if name=="":
                self.send {"action":"subscribe"}
            else:
                self.sendAndLog({"action":"subscribe", "name":name})

    def getClients(self):
        if self.socket:
            self.send({"action":"getClients"})

