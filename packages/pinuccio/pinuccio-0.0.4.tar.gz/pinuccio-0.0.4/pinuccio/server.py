import socket, json, time
from . import utils
from . import interface as sc
from .SThread import SThread
import uuid

notAllowedNames = ['', 'all']

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
    
    def send(self, connection, data, key=None):
        data = json.dumps(data)
        utils.debug("send:",data)
        sc.msg_send(connection, data)
    
    def recv(self, connection, key=None):
        try:
            data = sc.msg_recv(connection)
            utils.debug("recv:",data)
        except ConnectionResetError as e:
            return ""
        except ConnectionAbortedError as e:
            return ""
        except OSError as e:
            return ""
        
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            utils.debug("Error",data,"json Decode Error")
        return data
    
    def server_loop(self):
        while True:
            conn, addr = self.socket.accept()
            client_thread = SThread(target=self.client_startup)
            client_thread._args=(conn, client_thread)  # type: ignore
            client_thread.start()

    def client_startup(self, conn, thread):
        data = self.recv(conn)
        if data=="":
            exit(0)
        if not self.actionCheck(conn, data):
            self.closeSocket(conn)
            return

        if data["action"] == "subscribe":
            self.subscribeAction(conn, data, thread)
            utils.debug("clients:",self.connected_clients)
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
            if not self.actionCheck(conn, data):
                self.removeClient(name)
                exit(0)

            if data["action"] == "send":
                self.sendAction(conn, data, name)
            
            elif data["action"] == "getClients":
                self.getClientsAction(conn)
            
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
            self.closeSocket(self.connected_clients[name][0])
            del self.connected_clients[name]
            utils.debug("client",name,"disconnected")

    def stopThread(self, name):
        if name in self.connected_clients:
            thread = self.connected_clients[name][1]
            del self.connected_clients[name]
            thread.stop()

    def subscribeAction(self, conn, data, thread):
        client_name = None
        if "name" in data:
            client_name = data["name"]
            if client_name in self.connected_clients:
                self.sendStatus(conn, 454)
                return
            if client_name in notAllowedNames:
                self.sendStatus(conn, 453)
                return
        else:
            client_name = str(uuid.uuid4())
            while client_name in self.connected_clients:
                client_name = str(uuid.uuid4())

        self.connected_clients[client_name] = ([conn, thread])
        utils.debug("client",client_name,"connected")
        self.sendStatus(conn, 200)
        self.send(conn, {'action':'subscribeName', 'subscribeName':client_name})
        self.handle(conn, client_name)
    
    def closeAction(self, name):
        self.removeClient(name)

    def getClientsAction(self, conn):
        clients_name = [n for n in self.connected_clients]
        self.send(conn, {'action':'clientsList', 'clients':clients_name})

    def sendAction(self, conn, data, name):
        if "to" in data:
            dst_client = data["to"]
            if dst_client in self.connected_clients:
                if "msg" in data:
                    self.send(self.connected_clients[dst_client][0], {'action':'msg', 'msg':data['msg'], 'from':name})
                    self.sendStatus(conn, 200)
                else:
                    self.sendStatus(conn, 457)
            elif dst_client=="all":
                if "msg" in data:
                    for client in self.connected_clients:
                        self.send(self.connected_clients[client][0], {'action':'msg', 'msg':data['msg'], 'from':name})
                    self.sendStatus(conn, 200)
            else:
                self.sendStatus(conn, 456)
        else:
            self.sendStatus(conn, 455)

    def unknownAction(self, conn, data):
        self.sendStatus(conn, 459)

    def sendStatus(self, conn, status):
        self.send(conn, {'action':'status', 'status':status})

