#include <Arduino.h>
#include <SoftwareSerial.h>
#include "RS485_non_blocking.h"
void fWrite (const byte what);
int fAvailable ();
int fRead ();
void setup();
void loop();
#line 1 "src/my485Master.ino"
/*
    http://www.gammon.com.au/forum/?id=11428
*/
// #include "RS485_protocol.h"
//#include <SoftwareSerial.h>
//#include "RS485_non_blocking.h"


const byte ENABLE_PIN   = 3;
const byte LED_PIN      = 13;

SoftwareSerial rs485 (10, 11);  // receive pin, transmit pin

// callback routines

void fWrite (const byte what) {
    rs485.write (what);
}

int fAvailable () {
    return rs485.available ();
}

int fRead () {
    return rs485.read ();
}

void setup() {
    rs485.begin (28800);
    pinMode (ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);  // built-in LED
}  // end of setup

byte old_level = 0;
void sendMsg (const byte * data, const byte length);

void loop() {

    // read potentiometer
    byte level = analogRead (0) / 4;

    // no change? forget it
    if (level == old_level)
        return;

    // assemble message
    byte msg [] = {
                1,    // device 1
                2,    // turn light on
                level // to what level
            };

    // send to slave
    digitalWrite (ENABLE_PIN, HIGH);  // enable sending
    sendMsg (fWrite, msg, sizeof msg);
    digitalWrite (ENABLE_PIN, LOW);  // disable sending

    // receive response
    byte buf [10];
    byte received = recvMsg (fAvailable, fRead, buf, sizeof buf);

    digitalWrite (LED_PIN, received == 0);  // turn on LED if error

    // only send once per successful change
    if (received)
        old_level = level;

}  // end of loop