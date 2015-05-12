/*
    http://www.gammon.com.au/forum/?id=11428
*/
#include "my485Slave02.h"

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
    byte rcvdCMD;
    byte destADDR;

    nLoops++;
    if (nLoops > 30) {
        nLoops=0;
        Serial.print("\n\r");Serial.print(devName); Serial.print(" - Idle State! ");
    }

    byte rcvLen = recvMsg(fAvailable, fRead, buf, sizeof buf, timeOUT, DEBUG_TxRxMsg);

    if (rcvLen) {
        nLoops=0;
        Serial.print("\n\r");Serial.print(devName); Serial.print(" - Comando ricevuto       : ");printHex(buf, rcvLen, "");
        destADDR = buf[0];
        rcvdCMD  = buf[1];

        if (fDEBUG) {
            char DEBUG_TxRxLen = *DEBUG_TxRxMsg;           // byte 0
            Serial.print("\n\r");Serial.print(devName);Serial.print(" - DEBUG Comando ricevuto : ");printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
        }

        if (destADDR != myADDR) {
            Serial.print("      Address not point to me: ");Serial.println(destADDR);
            return;  // not my device
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
        Serial.print("\n\r");Serial.print(devName); Serial.print(" - Risposta inviata       : ");printHex(msg, sizeof(msg), " ");
        digitalWrite (ENABLE_PIN, LOW);  // disable sending


        if (fDEBUG) {
            char DEBUG_TxRxLen = *DEBUG_TxRxMsg;           // byte 0
            Serial.print("\n\r");Serial.print(devName);Serial.print(" - DEBUG Risposta inviata : ");printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
        }
        // analogWrite (11, buf [2]);  // set light level
    }  // end if something received

}  // end of loop

