#include <Arduino.h>
#include "dummy.h"
void setup();
void loop();
#line 1 "src/IAmArduino.ino"
//#include "dummy.h"

// const int ledPin = 12;


void setup(){
  Serial.begin(9600);
}

void loop(){
  Serial.println("Hello Pi - Io sono Arduino. Come va? (by LN)");
  delay(2000);
}
