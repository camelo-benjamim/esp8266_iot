import socket
import time
import json
import struct

ip = "192.168.0.15"
port = 5000
addr = ((ip,port))
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(addr)
time.sleep(1)
text = {'port': "D2", 'io': 'INPUT', 'value': 0, 'type': "DIGITAL"}
arr = json.dumps(text,indent=2).encode('utf-8')
client_socket.send(arr)
time.sleep(1)
recept = client_socket.recv(1024)
if recept == b'1':
    print("socket recebido")
    client_socket.close()

socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket2.connect((ip,5050))
porta = input("Digite a porta: ").encode('utf-8')
socket2.send(porta)
time.sleep(1)
print("enviado")
resposta = socket2.recv(1024)
print("resposta: " + str(resposta))
socket2.close()

