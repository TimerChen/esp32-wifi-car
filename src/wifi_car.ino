/*
 *  This sketch sends random data over UDP on a ESP32 device
 *
 */
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel rgb_display_16 = Adafruit_NeoPixel(4,16,NEO_GRB + NEO_KHZ800);    // 设置rgb引脚为16，串联4个彩灯

// WiFi network name and password:
const char * networkName = "your-ssid";
const char * networkPswd = "your-password";

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.0.255";
const int udpPort = 3333;

//Are we currently connected?
boolean connected = false;

//The udp library class
// WiFiUDP udp;

struct CarState
{
  /* data */
  uint8_t id, forward, backward, left, right, stop, speed, steer, brake, gear, mode, status, battery, temperature, timestamp, checksum;
  // uint8_t x;
  CarState(){
    stop = 1;
  }
};


class WiFiCar{
  WiFiUDP udp;
  CarState state;

  WiFiCar(uint8_t *id, const char * udpAddress, const int udpPort){
    state.id = id;
  }
  ~WiFiCar(){
    // send LEAVE to server
    udp.beginPacket(udpAddress, udpPort);
    udp.printf("[LEAVE]%d", state.id);
    udp.endPacket();
  }
  void init(){
    pinMode(27, OUTPUT);
    pinMode(13, OUTPUT);
  }
  void join(){
    // send JOIN to server
    udp.beginPacket(udpAddress, udpPort);
    udp.printf("[JOIN]%d", state.id);
    udp.endPacket();
    Serial.println("send join %d", state.id);
  }
  void send(uint8_t *data){
    // send data to server
    udp.beginPacket(udpAddress, udpPort);
    udp.printf("[DATA]%d", data);
    udp.endPacket();
  }
  void update(){
    // Recv a packet
    char data[128];
    udp.read(data, 128);
    Serial.println("recv data %s", data)
    if(data[0] == '[' && data[1] == 'D' && data[2] == 'A' && data[3] == 'T' && data[4] == 'A'){
      // parse data
      // data[5] = id
      // data[6] = x
      // data[7] = y
      // data[8] = z
      // data[9] = w
      // data[10] = speed
      // data[11] = steer
      // data[12] = brake
      // data[13] = gear
      // data[14] = mode
      // data[15] = status
      // data[16] = battery
      // data[17] = temperature
      // data[18] = timestamp
      // data[19] = checksum
      // data[20] = '\0'
      // update car
      state.forward = (data[6] == 1);
      state.stop = (data[6] == 0);
    }

    // change output to motor
    update_motor();

    rgb_display_16.show();
  }
  void update_motor(){
    if(state.stop){
      // stop motor
      analogWrite(27, 0);
      analogWrite(13, 0);
      rgb_display_16.setPixelColor(0, (((50 & 0xffffff) << 16) | ((200 & 0xffffff) << 8) | 50));
      return;
    }
    if(state.forward){
      analogWrite(27, 150);
      analogWrite(13, 0);
      rgb_display_16.setPixelColor(0, (((200 & 0xffffff) << 16) | ((50 & 0xffffff) << 8) | 50));
    }
  }
}car;

void setup(){
  // Initilize hardware serial:
  Serial.begin(115200);
  
  //Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);

  rgb_display_16.begin();
  rgb_display_16.setBrightness(5);

  car.init();
  car.join();
}

void loop(){
  //only send data when connected
  if(connected){
    //Recv a packet
    // udp.beginPacket(udpAddress,udpPort);
    // udp.printf("Seconds since boot: %lu", millis()/1000);
    // udp.endPacket();
    car.update();
  }
  //Wait for 1 second
  delay(10);
}

void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case ARDUINO_EVENT_WIFI_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          connected = true;

          // Set led to light
          rgb_display_16.setPixelColor(3, (((255 & 0xffffff) << 16) | ((255 & 0xffffff) << 8) | 255));
          rgb_display_16.show();
          break;
      case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;

          // set led to dark
          rgb_display_16.setPixelColor(3, (((0 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 0));
          rgb_display_16.show();
          break;
      default: break;
    }
}
