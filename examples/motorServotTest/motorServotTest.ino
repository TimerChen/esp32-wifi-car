
#include <Arduino.h>
#include "ESP32_Servo.h"

Servo servo_26;
Servo servo_25;
Servo servo_32;
Servo servo_33;

void setup(){
  Serial.begin(9600);
  Serial.println("hello");
  pinMode(27, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(15, OUTPUT);
  pinMode(14, OUTPUT);
  pinMode(12, OUTPUT);
  servo_26.attach(26,500,2500);
  servo_25.attach(25,500,2500);
  servo_32.attach(32,500,2500);
  servo_33.attach(33,500,2500);
}

void loop(){
  analogWrite(27, 0);
  analogWrite(13, 200);
  analogWrite(4, 0);
  analogWrite(2, 200);
  analogWrite(17, 0);
  analogWrite(15, 200);
  analogWrite(14, 0);
  analogWrite(12, 200);
  servo_26.write(0);
  delay(200);
  servo_25.write(0);
  delay(200);
  servo_32.write(0);
  delay(200);
  servo_33.write(0);
  delay(200);
  delay(1000);
  analogWrite(27, 150);
  analogWrite(13, 0);
  analogWrite(4, 150);
  analogWrite(2, 0);
  analogWrite(17, 150);
  analogWrite(15, 0);
  analogWrite(14, 150);
  analogWrite(12, 0);
  servo_25.write(180);
  delay(200);
  servo_26.write(180);
  delay(200);
  servo_32.write(180);
  delay(200);
  servo_33.write(180);
  delay(200);
  delay(1000);

}