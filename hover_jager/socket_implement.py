import socket
import time
import json
import struct
class SocketImplement:
    def __init__(self,ip,port_server):
        self.ip = ip
        self.port_server = port_server
        self.addr = ((self.ip,self.port_server))
        self.text = ''
        self.recept = ''
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(self.addr)
            time.sleep(1)
        except Exception as erro:
            return erro


class Socket1(SocketImplement):
    def __init__(self,ip,port_server):
        super().__init__(ip,port_server)

    def send_msg(self,port, io, value, type):
        try:
            port = port.upper()
            io = io.upper()
            value = int(value)
            type = type.upper()
            self.text = {'port': port, 'io': io, 'value': value, 'type': type}
            arr = json.dumps(self.text, indent=2).encode('utf-8')
            self.client_socket.send(arr)
            time.sleep(1)
            return 1
        except:
            return 0

    def return_msg(self):
        if self.client_socket.recv(1024) == b'1':
            self.client_socket.close()
            return 1
        else:
            return 0




class Socket2(SocketImplement):
    def __init__(self,ip,port_server):
        super().__init__(ip,port_server)

    def retornarSensor(self,sensor):
        resposta = ''
        self.client_socket.send(sensor.encode('utf-8'))
        resposta = self.client_socket.recv(1024)
        return str(resposta)