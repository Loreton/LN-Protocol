#include <Arduino.h>
#include <RS485_protocol.h>
#include <RS485_non_blocking.h>
#include <SoftwareSerial.h>
void fWrite(const byte what);
int  fAvailable ();
int  fRead ();
void setup();
void loop();
void printHex(const byte *data, const byte len);
#line 1 "src/my485Slave.ino"
/*
    http://www.gammon.com.au/forum/?id=11428
*/

//#include <RS485_protocol.h>
//#include <RS485_non_blocking.h>
//#include <SoftwareSerial.h>

// const byte ENABLE_PIN   =  4;
#define ENABLE_PIN      3
#define LED_PIN        13
#define RX_PIN         10
#define TX_PIN         11


const byte myADDR       = 1;

SoftwareSerial RS485 (RX_PIN, TX_PIN);  // receive pin, transmit pin

// callback routines
void fWrite(const byte what) {
    RS485.write (what);
}
int  fAvailable () {
    return RS485.available ();
}
int  fRead () {
    return RS485.read ();
}



void setup() {
    RS485.begin (9600);
    Serial.begin(9600);
    pinMode (ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN,    OUTPUT);  // built-in LED
}

// DEV=/dev/Arduino4 && ino build -m nano328 && ino upload -p $DEV -m nano328 && ino serial -p $DEV
void loop() {
    byte buf [10];
    unsigned long timeOUT = 10000;
    byte rcvdCMD;
    byte destADDR;

    byte rcvLen = recvMsg(fAvailable, fRead, buf, sizeof buf, timeOUT);
    if (rcvLen) {
        Serial.print("[Slave] - Comando ricevuto: ");printHex(buf, rcvLen);
        destADDR = buf[0];
        rcvdCMD  = buf[1];
        if (destADDR != myADDR) {
            Serial.print("      Address not point to me: ");Serial.println(destADDR);
            return;  // not my device
        }


        if (rcvdCMD != 2) {
            Serial.print("      Comando sconosciuto: ");Serial.println(buf[1]);
            return;  // unknown command
        }

        byte msg [] = {
           0,           // device 0 (master)
           myADDR,      // slaveAddress
           rcvdCMD,      // rcvdCMD
           3,           // data to be returned
           4,           // data to be returned
           5,           // data to be returned
        };
        byte msgSENT_DEBUG [100] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC
        delay (1000);  // give the master a moment to prepare to receive
        digitalWrite (ENABLE_PIN, HIGH);  // enable sending
        sendMsg (fWrite, msg, sizeof msg, msgSENT_DEBUG);
        Serial.print("[Slave] - Risposta inviata: ");printHex(msg, sizeof(msg));
        digitalWrite (ENABLE_PIN, LOW);  // disable sending

        // analogWrite (11, buf [2]);  // set light level
    }  // end if something received

}  // end of loop



void printHex(const byte *data, const byte len) {
    byte i;

    Serial.print("len:");
    Serial.print(len, DEC);
    Serial.print("  -  ");
    for (i=0; i<len; i++) {
        Serial.print(data[i], HEX);
        Serial.print(" ");
    }
    Serial.println("");
}