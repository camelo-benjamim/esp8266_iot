//HOVER JÄGER


//SOCKET SERVER
//DEFININDO REDE WIFI
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#define SSID "SEU SSID"
#define PASSWD "SENHA DO SSID"
#define SOCK_PORT 5000
WiFiServer sockServer(SOCK_PORT);
//armazenar resultado dos dados
String argument;
DynamicJsonDocument doc(2048);
//PORTAS DA ESP8266, ALTERAR CASO HAJA MUDANÇA NO HARDWARE
char ports[] = "{\"D0\": 16, \"D1\": 5, \"D2\": 4, \"D3\": 0, \"D4\": 2, \"D5\": 14, \"D6\": 12, \"D7\": 13, \"D8\": 15, \"A0\": 17}";
DynamicJsonDocument ports_map(1024);
void setup(){
    Serial.begin(115200);
    delay(1000);
    deserializeJson(ports_map, ports);
    WiFi.begin(SSID,PASSWD);
    while (WiFi.status() != WL_CONNECTED){delay(100);}
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    sockServer.begin();
    
}

void loop(){
    
    WiFiClient client = sockServer.available();
    if (client){
        while (client.connected()){
            while (client.available() > 0){
                char value = client.read();
                parseArgument(value);
                client.stop(); //acabou a leitura dos dados. Finaliza o client.
            }
            Serial.println("buf: ");
            int str_len = argument.length() + 1; 
            // Prepare the character array (the buffer) 
            char char_array[str_len];
            // Copy it over 
            argument.toCharArray(char_array, str_len);
            deserializeJson(doc, argument);
            String pino = doc["port"];
            String io = doc["io"];
            String value = doc["value"];
            String type = doc["type"];
            //Escolhendo tipo de pino
            if (String(type) == "DIGITAL"){
              Serial.println("Tipo digital escolhido");
              if (String(io) == "INPUT"){
              //transformar valor do pino para char de alguma maneira e armazenar em value
              int pin_go = ports_map[pino];
              pinMode(pin_go,INPUT);
              digitalRead(pin_go);
            }
            else {
              int pin_go = ports_map[pino];
              pinMode(pin_go,OUTPUT);
              int valor = value.toInt();
                if (valor == 0){
                  digitalWrite(pin_go,LOW);
                }
                else{
                  digitalWrite(pin_go,HIGH);
                }
            }
            }
            //CASO SEJA ANALÓGICO
            else if (String(type) == "ANALOG") {
              Serial.println("Tipo analógico escolhido");
              if (String(io) == "INPUT"){
                //transformar valor do pino para char de alguma maneira e armazenar em value
                int pin_go = ports_map[pino];
                pinMode(pin_go,INPUT);
                analogRead(pin_go);
                                        }
            else {
              int pin_go = ports_map[pino];
              pinMode(pin_go,OUTPUT);
              int valor = value.toInt();
               
              analogWrite(pin_go,valor);
              }
            }
            
            //construir para pinos analógicos
            delay(1000);
          
        }
        
    }
    cleanVariable();
}

void parseArgument(char x_argument){
  argument = argument + x_argument;
}
void cleanVariable(){
  argument = "";
}
