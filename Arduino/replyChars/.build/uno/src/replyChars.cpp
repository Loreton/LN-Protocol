#include <Arduino.h>

void setup();
void loop();
#line 1 "src/replyChars.ino"
int incomingByte = 0;   // for incoming serial data
// int ledPin = 4;   /

void setup(){
    // pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop(){
        // send data only when you receive data:
    if (Serial.available() > 0) {
        // read the incoming byte:
        incomingByte = Serial.read();
        delay(50);
        // say what you got:
        Serial.print("I received: ");
        Serial.println(incomingByte, DEC);
    }
    delay(500);
}
