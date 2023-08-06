import struct
from sys import getsizeof


"""
PACKET STRUCTURE

1Byte + NByte + CByte
  N   +   C   + data

Max N value = (2^8) = 256
Max N value = (2^(256*8)) = (2^(2048))
Max data byte = (2^(2048))

"""


BYTES_OBJECT_OVERHEAD = getsizeof(b"")

types = {
    "<B":1,
    "<H":2,
    "<L":4,
    "<Q":8
}




class msg_send_Exception(Exception):
    def __init__(self, message="Error"):
        super().__init__(message)

class msg_recv_Exception(Exception):
    def __init__(self, message="Error"):
        super().__init__(message)



def msg_recv(socket):
    try:
        N = socket.recv(1)
    except ConnectionResetError as e:
        raise e
    except ConnectionAbortedError as e:
        raise e
    except OSError as e:
        raise e
    
    if N == b"":
        raise msg_recv_Exception("Socket closed")
    N = struct.unpack('<B', N)[0]

    if N != 0:
        C = recvNBytes(socket, N)
        for t in types:
            if types[t] == N:
                C = struct.unpack(t, C)[0]
        
        if C != 0:
            data = recvNBytes(socket, C)
            data = data.decode('utf-8')
        else:
            raise msg_recv_Exception("Error reciving C")
    
    else:
        raise msg_recv_Exception("Error reciving N")
    
    return data


def msg_send(socket, data):
    if type(data) is not str:
        raise msg_send_Exception("'data' must be string")
    if data == "":
        raise msg_send_Exception("'data' must not be empty")

    data = data.encode("utf-8")
    C = int(len(data))
    N = (C.bit_length()+7)//8

    if N>8:
        raise msg_send_Exception("Message too long")

    for t in types:
        if N<=types[t]:
            socket.send(struct.pack('<B', types[t]))
            socket.send(struct.pack(t, C))
            socket.send(data)
            return None

    raise msg_send_Exception("Error in msg_send")
    

def recvNBytes(socket, N):
    data = socket.recv(N)
    while getsizeof(data)-BYTES_OBJECT_OVERHEAD!=N:
        data += socket.recv(N-getsizeof(data)+BYTES_OBJECT_OVERHEAD)
    return data


def msg_encode(data, key):
    pass


def msg_decode(data, key):
    pass

