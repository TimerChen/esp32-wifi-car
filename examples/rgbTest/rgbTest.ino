/**
 * 使用前，先导入Adafruit_NeoPixel库
 */
#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel rgb_display_16 = Adafruit_NeoPixel(4,16,NEO_GRB + NEO_KHZ800);    // 设置rgb引脚为16，串联4个彩灯

void setup(){
  rgb_display_16.begin();
}

void loop(){
  rgb_display_16.setBrightness(20);
  rgb_display_16.setPixelColor((1)-1, (((0 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 255));   // 设置rgb彩灯为蓝色
  rgb_display_16.setPixelColor((2)-1, (((0 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 255));
  rgb_display_16.setPixelColor((3)-1, (((0 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 255));
  rgb_display_16.setPixelColor((4)-1, (((0 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 255));
  rgb_display_16.show();
  delay(1000);
  rgb_display_16.setPixelColor((1)-1, (((255 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 0));   // 设置rgb彩灯为红色
  rgb_display_16.setPixelColor((2)-1, (((255 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 0));
  rgb_display_16.setPixelColor((3)-1, (((255 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 0));
  rgb_display_16.setPixelColor((4)-1, (((255 & 0xffffff) << 16) | ((0 & 0xffffff) << 8) | 0));
  rgb_display_16.show();
  delay(1000);
  rgb_display_16.setPixelColor((1)-1, (((0 & 0xffffff) << 16) | ((255 & 0xffffff) << 8) | 0));   // 设置rgb彩灯为绿色
  rgb_display_16.setPixelColor((2)-1, (((0 & 0xffffff) << 16) | ((255 & 0xffffff) << 8) | 0));
  rgb_display_16.setPixelColor((3)-1, (((0 & 0xffffff) << 16) | ((255 & 0xffffff) << 8) | 0));
  rgb_display_16.setPixelColor((4)-1, (((0 & 0xffffff) << 16) | ((255 & 0xffffff) << 8) | 0));
  rgb_display_16.show();
  delay(1000);
}
