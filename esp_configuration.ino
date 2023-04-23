//ESP8266-IOT
//PROGRAMADOR: BENJAMIM CAMÊLO
//DATA 3/2022
//UTILIDADE: UTILIZANDO SOCKET PARA "CONVERSAR" COM UMA APLICAÇÃO PYTHON QUE DÁ COMANDOS SOBRE AS PORTAS DA ESP8266
//LICENSA: MIT 
//AUTORIZO O USO PARA OS MAIS DIVERSOS MEIOS MODIFICAÇÃO E COMPARTILHAMENTO DO SOFTWARE. SEGUINDO A LICENSA DE CÓDIGO ABERTO MIT

//SOCKET SERVER
//DEFININDO REDE WIFI
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#define SSID "brisa-2504601"
#define PASSWD "vao1zmbs"
#define SOCK_PORT 5000
#define SOCK_PORT2 5050
//PELO SOCKET 1 PASSAR COMANDOS PARA ABRIR E FECHAR PORTAS E RETORNAR 1 CASO TENHA OCORRIDO TUDO BEM
WiFiServer sockServer(SOCK_PORT);
WiFiServer sockServer2(SOCK_PORT2);
//armazenar resultado dos dados
DynamicJsonDocument doc(2048);
//PORTAS DA ESP8266, ALTERAR CASO HAJA MUDANÇA NO HARDWARE
char ports[] = "{\"D0\": 16, \"D1\": 5, \"D2\": 4, \"D3\": 0, \"D4\": 2, \"D5\": 14, \"D6\": 12, \"D7\": 13, \"D8\": 15, \"A0\": 17}";
DynamicJsonDocument ports_map(1024);
DynamicJsonDocument ports_io(1024);
//IMPLEMENTAR PORTAS IO
String argumentsPrintable;
String argument;
String variablearm;
int readingSensorValue;
void setup(){
    Serial.begin(115200);
    delay(1000);
    //PARA O INÍCIO CORRETO, INICIAREMOS TODAS AS PORTAS COMO OUTPUT E VALUE =0
    //PORTA D0:
    pinMode(16,OUTPUT);
    digitalWrite(16,LOW);
    //PORTA D1:
    pinMode(5,OUTPUT);
    digitalWrite(5,LOW);
    //PORTA D2:
    pinMode(4,OUTPUT);
    digitalWrite(4,LOW);
    //PORTA D3:
    pinMode(0,OUTPUT);
    digitalWrite(0,LOW);
    //PORTA D4:
    pinMode(2,OUTPUT);
    digitalWrite(2,LOW);
    //PORTA D5:
    pinMode(14,OUTPUT);
    digitalWrite(14,LOW);
    //PORTA D6:
    pinMode(12,OUTPUT);
    digitalWrite(12,LOW);
    //PORTA D7:
    pinMode(13,OUTPUT);
    digitalWrite(13,LOW);
    //PORTA D8:
    pinMode(15,OUTPUT);
    digitalWrite(15,LOW);
    //PORTA A0:
    pinMode(17,OUTPUT);
    analogWrite(17,0);
    //
    //SERIALIZANDO PORTAS PARA JSON
    deserializeJson(ports_map, ports);
    WiFi.begin(SSID,PASSWD);
    while (WiFi.status() != WL_CONNECTED){delay(100);}
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    //INICIANDO OS SERVIDORES SOCKET
    sockServer.begin();
    sockServer2.begin();
}

void loop(){
    //INICIANDO SOCKET 1
    WiFiClient client = sockServer.available();
    if (client){
        while (client.connected()){
          
            while (client.available() > 0){
                char value = client.read();
                //INICIANDO ESCUTA
                parseArgument(value);
                //CASO TENHA FUNCIONADO CORRETAMENTE TERÁ b'1' COMO RETORNO
                client.println(1);
                client.stop();
            }
            //
            int str_len = argument.length() + 1; 
            char char_array[str_len];
            argument.toCharArray(char_array, str_len);
            deserializeJson(doc, argument);
            //PEGANDO VALORES PASSADOS PARA O JSON
            String pino = doc["port"];
            String io = doc["io"];
            String value = doc["value"];
            String type = doc["type"];
            //SALVANDO TIPOS
            ports_io[pino]= value;
            serializeJson(ports_io, argumentsPrintable);
            //Escolhendo tipo de pino
            //ANALISANDO CONDIÇÕES (DIGITAL E ANALOG)
            if (String(type) == "DIGITAL"){
              Serial.println("Tipo digital escolhido");
              if (String(io) == "INPUT"){
              int pin_go = ports_map[pino];
              pinMode(pin_go,INPUT);
              digitalRead(pin_go);
              //TESTAR AQUI
              ports_io[pino] = "INPUT";
              serializeJson(ports_io, argumentsPrintable);
              //
            }
            else {
              int pin_go = ports_map[pino];
              pinMode(pin_go,OUTPUT);
              int valor = value.toInt();
              digitalWrite(pin_go,valor);
              ports_io[pino] = "OUTPUT";
              serializeJson(ports_io, argumentsPrintable);
            }
            }
            //CASO SEJA ANALÓGICO
            else if (String(type) == "ANALOG") {
              if (String(io) == "INPUT"){
                //transformar valor do pino para char de alguma maneira e armazenar em value
                //TESTAR AQUI
                int pin_go = ports_map[pino];
                ports_io[pino] = "INPUT";
                serializeJson(ports_io, argumentsPrintable);
                pinMode(pin_go,INPUT);
                analogRead(pin_go);
                                        }
            else {
              int pin_go = ports_map[pino];
              ports_io[pino] = "OUTPUT";
              serializeJson(ports_io, argumentsPrintable);
              pinMode(pin_go,OUTPUT);
              int valor = value.toInt();
              analogWrite(pin_go,valor);
              }
            }
            
            //construir para pinos analógicos
            delay(100);
          
        }
        
        
    }
    cleanVariable();
    


    //INICIANDO O SOCKET 2: 
    //O SOCKET 2 SERVE PARA LEITURA DE VARIÁVEIS
    variablearm = "";
    WiFiClient client2 = sockServer2.available();
    if (client2){
        while (client2.connected()){
            while (client2.available() > 0){
                int contador = 0;
                while (contador <= 1) {
                  char value = client2.read();
                  valueParsing(value);
                  contador = contador + 1;
                }
                //PASSANDO VALORES INPUT E OUTPUT PARA LISTA QUE RELACIONA PORTA(VALOR) E I/O
                if (ports_io[variablearm] == "INPUT"){
                  int leitura = ports_map[variablearm];
                  if (ports_map[variablearm] == "DIGITAL"){
                    readingSensorValue = digitalRead(leitura);
                  }
                  else{
                    readingSensorValue = analogRead(leitura);
                  }
                }
                else {
                  //PROIBIDO
                  readingSensorValue = -1;
                  
                }
                client2.println(readingSensorValue);
                //
                client2.stop();
                break;
                
                
                //descubra uma meneira de passar para o app python o resultado...
            }
           
        }
        
    }
    
    
    

    
}

void parseArgument(char x_argument){
  argument = argument + x_argument;
}
void cleanVariable(){
  argument = "";
  
}

void valueParsing(char value){
  variablearm = variablearm + value;
}
