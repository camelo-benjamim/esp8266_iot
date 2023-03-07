//HOVER JÄGER



//SOCKET SERVER
//DEFININDO REDE WIFI
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#define SSID "brisa-2511595"
#define PASSWD "v4mdefk8"
#define SOCK_PORT 5000
WiFiServer sockServer(SOCK_PORT);
//armazenar resultado dos dados
String argument;
DynamicJsonDocument doc(2048);
void setup(){
    Serial.begin(115200);
    delay(1000);
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
            Serial.println("argument :");
            deserializeJson(doc, argument);
            String pino = doc["port"];
            String io = doc["io"];
            String value = doc["value"];
            //construido para pinos digitais...
            if (String(io) == "INPUT"){
              //transformar valor do pino para char de alguma maneira e armazenar em value
              int pin_go = pino.toInt();
              pinMode(pin_go,INPUT);
              digitalWrite(pin_go,LOW);
            }
            else {
              int pin_go = pino.toInt();
              pinMode(pin_go,OUTPUT);
              int valor = value.toInt();
              if (valor == 0){
                digitalWrite(pin_go,LOW);
              }
              else{
                digitalWrite(pin_go,HIGH);
              }
            }
            //construir para pinos analógicos
            Serial.println("pino: ");
            Serial.println(pino);
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
