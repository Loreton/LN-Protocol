/*
    http://www.gammon.com.au/forum/?id=11428

*/
#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <RS485_protocol.h>
#include <RS485_non_blocking.h>
#include <SoftwareSerial.h>

#include "RS-485_Monitor.h"                      //  pin definitions




SoftwareSerial RS485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

// callback routines
void fWrite(const byte what) {RS485.write (what); }
int  fAvailable ()          {return RS485.available (); }
int  fRead ()               {return RS485.read (); }



void setup() {
    Serial.begin(9600);
    RS485.begin (9600);
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);  // built-in LED
}



void loop() {
    byte SLEEP_TIME=10;
    byte level = 0;
    for (level=0; level<=255; level++) {
        Serial.println("");

        if (LnRcvMessage(10000)) {
            Serial.print("\r\n[Monitor] - Working on response data. Sleeping for ");
            Serial.print(SLEEP_TIME, DEC);
            Serial.println("");
        }
        delay(SLEEP_TIME*1000);
    }
}


bool fDEBUG = true;
/* --------------------
    mi serve per verificare i dati e l'ordine con cui sono
    stati inviati inclusi STX, CRC, ETX
    DEBUG_sentMsg[0] contiene lunghezza dei dati
-------------------- */
byte DEBUG_TxRxMsg [200] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC



// #############################################################
// #
// #############################################################
byte LnRcvMessage(unsigned long timeOUT) {
    // receive response
    byte rxData [50];

    byte rxDataLen = recvMsg (fAvailable, fRead, rxData, sizeof rxData, timeOUT, DEBUG_TxRxMsg);
    digitalWrite (LED_PIN, rxDataLen == 0);  // turn on LED if error


    if (fDEBUG) {
        // char DEBUG_SentMsgLen = *DEBUG_sentMsg;           // byte 0
        char DEBUG_RxLen = *DEBUG_TxRxMsg;           // byte 0
        if (DEBUG_RxLen > 0) {
            Serial.print("\r\n[Monitor] - DEBUG Risposta ricevuta : ");
            printHex(&DEBUG_TxRxMsg[1], DEBUG_RxLen, " - [STX ...data... CRC ETX]");
        }
            Serial.print("\r\n[Monitor] - DEBUG No data received during: ");
            Serial.print(timeOUT);
            Serial.print("ms");
    }

    else {
        if (rxDataLen > 0) {
            Serial.print("\r\n[Monitor] - Risposta ricevuta       : ");
            printHex(rxData, rxDataLen, "");
        } else {
            Serial.print("\r\n[Monitor] - TIMEOUT waiting response. len=");
            printHex(rxData, rxDataLen, "");
        }
    }
    return rxDataLen;
}



