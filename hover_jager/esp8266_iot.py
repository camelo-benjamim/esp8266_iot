import time

import socket_implement as si

##implementando valores conforme foi feito na esp8266

socket1 = si.Socket1("192.168.0.15",5000)
socket2 = si.Socket2("192.168.0.15",5050)


class Playing:
    def play(self,port,io,value,type):
        try:
            message_send = socket1.send_msg(port,io,value,type)
            retorno = socket1.return_msg()
            while not (message_send and retorno == 1):
                message_send = socket1.send_msg(port, io, value, type)
                retorno = socket1.return_msg()
                time.sleep(1)
        except:
            pass


    def sensorRead(self,port):
        result = socket2.retornarSensor(port)
        print(result)
        result = ''
print("executando 1 :")
led = Playing()
led.play('D3','INPUT',0,'DIGITAL')

print("executando 2: ")
p = Playing()
res = p.sensorRead("D2")



