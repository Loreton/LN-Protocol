/*
    http://www.gammon.com.au/forum/?id=11428
*/
#include "my485Slave.h"

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


bool fDEBUG = false;
// #define RCV_ERROR      1
// #define RCV_TIMEOUT    2

// DEV=/dev/Arduino4 && ino build -m nano328 && ino upload -p $DEV -m nano328 && ino serial -p $DEV
void loop() {
    byte buf [10];
    byte rcvdCMD;
    byte destADDR;
    byte fromADDR;

    nLoops++;
    if (nLoops > 30) {
        nLoops=0;
        Serial.print(devName); Serial.println(" - Idle State! ");
    }

    byte rcvLen = recvMsg(fAvailable, fRead, buf, sizeof buf, timeOUT, DEBUG_TxRxMsg);

        // - Controllo di eventuali ERRORI oppure come DEBUG per visualizzare dati ricevuti errati
    Serial.print("rcvLen:");Serial.println(rcvLen);
    if ( (rcvLen == RCV_ERROR) || (rcvLen == RCV_BADCRC) || (rcvLen == RCV_BADCHAR) || (fDEBUG == true) ) {
        char DEBUG_TxRxLen = *DEBUG_TxRxMsg;           // byte 0
        if (DEBUG_TxRxLen != 0) {
            Serial.print(devName);
            Serial.print(" - DEBUG Dati ricevuti    : ");
            printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]\n\r"); // contiene LEN STX ...data... ETX
        }
        if (rcvLen == 1) {    // in caso di dati in errrore non proseguiamo
            rcvLen = 0;
            // Serial.print("\n\r");
        }
    }

    if (rcvLen) {
        nLoops=0;
        Serial.print(devName); Serial.print(" - Comando ricevuto       : ");printHex(buf, rcvLen, "\n\r");
        destADDR = buf[0];

        if (destADDR == 0) {
            fromADDR = buf[1];
            Serial.print("            Packet from Slave device: ");Serial.print(fromADDR); Serial.println("    -  to Master device: 0");
            return;  // not my device
        }

        if (destADDR != myADDR) {
            Serial.print("            Packet from Master device: 0"); Serial.print("   -  to Slave device: ");Serial.println(destADDR);
            return;  // not my device
        }

        rcvdCMD  = buf[1];
        byte msg [] = {
           0,           // device 0 (master)
           myADDR,      // slaveAddress
           rcvdCMD,      // rcvdCMD
           3,           // data to be returned
           4,           // data to be returned
           5,           // data to be returned
        };
        // byte msgSENT_DEBUG [100] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC
        delay (1000);  // give the master a moment to prepare to receive
        digitalWrite (ENABLE_PIN, HIGH);  // enable sending
        sendMsg (fWrite, msg, sizeof msg, DEBUG_TxRxMsg);
        Serial.print(devName); Serial.print(" - Risposta inviata       : ");printHex(msg, sizeof(msg), "\n\r");
        digitalWrite (ENABLE_PIN, LOW);  // disable sending


        if (fDEBUG) {
            char DEBUG_TxRxLen = *DEBUG_TxRxMsg;           // byte 0
            // Serial.print("\n\r");
            Serial.print(devName);Serial.print(" - DEBUG Risposta inviata : ");printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]\n\r"); // contiene LEN STX ...data... ETX
        }

        Serial.print("\n\r");
        // analogWrite (11, buf [2]);  // set light level
    }  // end if something received

}  // end of loop

