#include <Arduino.h>

void setup();
void loop();
void printChars();
#line 1 "src/replyChars.ino"
int incomingByte = 0;   // for incoming serial data
// int ledPin = 4;   /

void setup(){
    // pinMode(ledPin, OUTPUT);
    Serial.begin(9600);
}

void loop(){
    printChars();
    /*
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
    */
}


/*
Uses a FOR loop for data and prints a number in various formats.
*/


void printChars() {
int x = 0;    // variable
  // print labels
    String label = "UNFMT";
    label.concat(" \t DEC \t HEX \t OCT \t BIN");
    // Serial.print("UNFMT \t DEC \t HEX \t OCT \t BIN");       // prints a label
    Serial.println(label);       // prints a label

    for(x=0; x< 64; x++){    // only part of the ASCII chart, change to suit

        // print it out in many formats:
        Serial.print(x);       // print as an ASCII-encoded decimal - same as "DEC"
        Serial.print("\t");    // prints a tab

        Serial.print(x, DEC);  // print as an ASCII-encoded decimal
        Serial.print("\t");    // prints a tab

        Serial.print(x, HEX);  // print as an ASCII-encoded hexadecimal
        Serial.print("\t");    // prints a tab

        Serial.print(x, OCT);  // print as an ASCII-encoded octal
        Serial.print("\t");    // prints a tab

        Serial.println(x, BIN);  // print as an ASCII-encoded binary
        //                             then adds the carriage return with "println"
        delay(200);            // delay 200 milliseconds
    }
    Serial.println("");      // prints another carriage return
}
