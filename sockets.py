import socket
import time
import json
import struct
class Socket1:
    def __init__(self,ip,port_socket,port,io,value,tipo):
        self.ip = ip
        self.port_socket = port_socket
        self.port = port
        self.io = io
        self.value = value
        self.tipo = tipo
        addr = ((self.ip,self.port_socket))
        try:
            socket.socket()
        except:
            pass
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(addr)
            time.sleep(1)
            text = {'port': port, 'io': io, 'value': value, 'type': tipo}
            arr = json.dumps(text,indent=2).encode('utf-8')
            self.client_socket.send(arr)
            time.sleep(1)
            recept = self.client_socket.recv(1024)
            if recept == b'1':
                self.status = True
            else:
                self.status = False
        except socket.error as err:
            print(err)
        finally:
            self.client_socket.close()

    
class Socket2:
    def __init__(self,ip,port_socket,port_read):
        c_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        c_socket.connect((ip,port_socket))
        porta = port_read.encode('utf8')
        c_socket.send(porta)
        time.sleep(1)
        self.resposta = c_socket.recv(1024)
        c_socket.close()

    def retorno(self):
        return self.resposta.decode('utf-8')