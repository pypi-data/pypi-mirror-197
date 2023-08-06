import socket, json, time
from . import utils
from . import interface as sc
from .SThread import SThread



class Server():
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.socket = None
        self.connected_clients = {}

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()
        self.server_loop()
    
    @classmethod
    def send(cls, connection, data, key=None):
        data = json.dumps(data)
        sc.msg_send(connection, data)
    
    @classmethod
    def recv(cls, connection, key=None):
        try:
            data = sc.msg_recv(connection)
        except ConnectionResetError as e:
            return ""
        
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            utils.debug(data,"json Decode Error")
        return data
    

    def server_loop(self):
        while True:
            conn, addr = self.socket.accept()
            client_thread = SThread(target=self.client_startup)
            client_thread._args=(conn, client_thread)  # type: ignore
            client_thread.start()

    def client_startup(self, conn, thread):
        utils.debug(self.connected_clients)
        data = self.recv(conn)
        if data=="":
            exit(0)
        if not self.actionCheck(conn, data):
            self.closeSocket(conn)
            return

        if data["action"] == "subscribe":
            self.subscribeAction(conn, data, thread)
        else:
            self.sendStatus(conn, 458)
            self.closeSocket(conn)
            return
    
    def handle(self, conn, name):
        while True:
            data = self.recv(conn)
            if (data==""):
                self.removeClient(name)
                exit(0)
            utils.debug(data)
            if not self.actionCheck(conn, data):
                self.removeClient(name)
                exit(0)

            if data["action"] == "send":
                self.sendAction(conn, data)
            
            elif data["action"] == "close":
                self.closeAction(conn, data)
                exit(0)
            
            else:
                self.unknownAction(conn, name)

    def actionCheck(self, conn, data):
        if type(data) is not dict:
            self.sendStatus(conn, 451)
            return False
        if "action" not in data:
            self.sendStatus(conn, 452)
            return False
        return True

    def closeSocket(self, conn):
        conn.close()
    
    def removeClient(self, name):
        if name in self.connected_clients:
            #self.send(self.connected_clients[name][0], '{"Info":"Socket Closed"}')
            self.closeSocket(self.connected_clients[name][0])
            del self.connected_clients[name]
            utils.debug(name,"disconnected")

    def stopThread(self, name):
        if name in self.connected_clients:
            thread = self.connected_clients[name][1]
            del self.connected_clients[name]
            thread.stop()

    def subscribeAction(self, conn, data, thread):
        if "name" in data:
            client_name = data["name"]
            if client_name not in self.connected_clients:
                self.connected_clients[client_name] = ([conn, thread])
                utils.debug(client_name,"connected")
                self.sendStatus(conn, 200)
                self.handle(conn, client_name)
            else:
                self.sendStatus(conn, 454)
                self.closeSocket(conn)
        else:
            self.sendStatus(conn, 453)
            self.closeSocket(conn)

    def closeAction(self, name):
        self.removeClient(name)

    def sendAction(self, conn, data):
        if "to" in data:
            dst_client = data["to"]
            if dst_client in self.connected_clients:
                if "msg" in data:
                    self.send(self.connected_clients[dst_client][0], {"msg":data["msg"]})
                    self.sendStatus(conn, 200)
                else:
                    self.sendStatus(conn, 457)
            else:
                self.sendStatus(conn, 456)
        else:
            self.sendStatus(conn, 455)

    def unknownAction(self, conn, data):
        self.sendStatus(conn, 459)

    def sendStatus(self, conn, status):
        self.send(conn, '{"status":'+str(status)+'}')

