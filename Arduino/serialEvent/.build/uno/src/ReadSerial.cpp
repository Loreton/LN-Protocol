#include <Arduino.h>

void setup();
void loop();
void serialEvent();
#line 1 "src/ReadSerial.ino"
/*
  Serial Event example

 When new serial data arrives, this sketch adds it to a String.
 When a newline is received, the loop prints the string and
 clears it.

 A good test for this is to try it with a GPS receiver
 that sends out NMEA 0183 sentences.

 Created 9 May 2011
 by Tom Igoe

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/SerialEvent

 */

String inputBuffer = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

void setup() {
    // initialize serial:
    Serial.begin(9600);
    // reserve 200 bytes for the inputBuffer:
    inputBuffer.reserve(200);
}

void loop() {
        // print the string when a newline arrives:
    if (stringComplete) {
        Serial.println(inputBuffer);
        // clear the string:
        inputBuffer = "";
        stringComplete = false;
    }
}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
    while (Serial.available()) {

        // get the new byte:
        char inChar = (char)Serial.read();

        // add it to the inputBuffer:
        inputBuffer += inChar;

        // if the incoming character is a newline, set a flag
        // so the main loop can do something about it:
        if (inChar == '\n') {
            stringComplete = true;
        }
    }
}