/*
Author:     Loreto Notarantonio
version:    LnVer_2017-05-08_10.17.16

Scope:      Funzione di relay. Prende i dati provenienti da una seriale collegata a RaspBerry
            ed inoltra il comando sul bus RS485.
            Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/

#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <LnRS485_protocol.h>
#include <SoftwareSerial.h>


#include "RS-485_Relay.h"                      //  pin definitions
// definiti nel .h
// HardwareSerial & serialPi = Serial; // rename della Serial per comodità
// SoftwareSerial  arduino485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

#include <EEPROM.h>


// ------ RS485 callback routines
// void arduinofWrite(const byte what)   {       Serial485.write (what); }
// int  arduinofAvailable()              {return Serial485.available (); }
// int  arduinofRead()                   {return Serial485.read (); }

// ------ RS485 callback routines
// void pifWrite(const byte what)   {       piSerial.write (what); }
// int  pifAvailable()              {return piSerial.available (); }
// int  pifRead()                   {return piSerial.read (); }

#define ENA_TX       HIGH
#define ENA_RX       LOW
#define DIS_TX       LOW

byte        myEEpromAddress;        // who we are
RXTX_DATA   RxTx, *pData;             // struttura dati
//.............0 1 234567890123
char myID[] = "\r\n[xxx] - "; // i primi due byte saranno CR e LF
/*
      .............01234567890123
    char myID[] = "rn[xxx] - "; // i primi due byte saranno CR e LF
      ............. 0 1 234567890123
    char myID[] = "\r\n[xxx] - "; // i primi due byte saranno CR e LF
*/
unsigned long responseDelay = 0;



//python3.4 -m serial.tools.list_ports
void setup() {
        // -----------------------------
        // inizializzazione bus RS485
        // e relativa struttura dati
        // -----------------------------
    arduino485.begin(9600);
    pData               = &RxTx;
    pData->displayData  = false;    // data display dei byt hex inviatie ricevuti (lo fa direttamente la libreria)
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // enable rx by default
    digitalWrite(RS485_ENABLE_PIN, ENA_RX);  // set in receive mode

        // -----------------------------
        // inizializzazione porta seriale
        // di comunicazione con raspBerry
        // -----------------------------
    serialPi.begin(9600);             // SERIAL_8N1 (the default)

        // --------------------------------------------
        // preparazione myID con indirizzo di Arduino
        // 1. convert integer myAddress to string
        // 2. copy string into myID array
        // --------------------------------------------
    myEEpromAddress = EEPROM.read(0);
    char *xx = LnUtoa(myEEpromAddress, 3, '0');
    // myID[0] = 13;   // CR
    // myID[1] = 10;   // NL
    myID[3] = xx[0];
    myID[4] = xx[1];
    myID[5] = xx[2];
    pData->myID = myID;

    // piSerial.println(myID);

    /* ----
        bit_time = 1/baud_rate
        At 9600, bit time is 104.166666666666 microseconds.

        For example 9600 8 N 1 uses 10 bits per word (1 start bit, 8 data bits, and 1 stop bit).
        Each word  would take      10/9600 =0.00104167 sec --> 1.0417mS --> 1041.66666666 uS
        100  words would take (100*10)/9600=0,104167   sec --> 104.17 ms
        Quindi per evitare sovrapposizioni nelle risposte e assumendo che
        gli indirizzi partono da 11...
        ...calcolo il delay con (eepromAddress-10)*500
    ---- */
    responseDelay = (myEEpromAddress-10)*500; // Es.: Addr 12, delay = (12-10)*500=1000mS

    pinMode (LED_PIN, OUTPUT);          // built-in LED

}


// ################################################################
// #
// ################################################################
void loop() {

    /*
    pData->timeout = 10000;
    byte rCode = recvMsgPi(pData);
    if (rCode == LN_OK) {
        processRequest(pData);
        Serial.println();
    }
    */

    pData->rx[SEQNO_HIGH] = 0;
    pData->rx[SEQNO_LOW]  = 1;

    serialPi.print(F("   (Request is for me) ... answering"));
    byte response[] = "Loreto....";

    sendMessage(11, response, sizeof(response), pData);
    delay(5000);

    /*
    pData->timeout = 10000;
    byte rCode = recvMsg (arduinofAvailable, arduinofRead, pData);

    if (rCode == LN_OK) {
        processRequest(pData);
        Serial.println();
    }

    // else if (pData->rx[0] == 0) {
    //     Serial.print(myID);
    //     Serial.print(F("rCode: "));Serial.print(rCode);
    //     Serial.print(F(" - Nessuna richiesta ricevuta in un tempo di mS: "));
    //     Serial.print(pData->timeout);
    //     Serial.println();
    // }

    else {
        rxDisplayData(rCode, pData);
        Serial.println();
    }
    */
}

// #############################################################
// #
// #############################################################
void processRequest(RXTX_DATA *pData) {
    byte senderAddr = pData->rx[SENDER_ADDR];
    byte destAddr   = pData->rx[DESTINATION_ADDR];
    int seqNO       = pData->rx[SEQNO_HIGH]*256 + pData->rx[SEQNO_LOW];

    Serial.print(myID); Serial.print(F("inoRECV from: ")); Serial.print(senderAddr);
                        Serial.print(F(" to  : ")); Serial.print(destAddr);
                        Serial.print(F(" [")); Serial.print(LnUtoa(seqNO,5,'0'));Serial.print(F("]"));

    if (destAddr == myEEpromAddress) {    // sono io.... rispondi sulla RS485
        Serial.print(F("   (Request is for me) ... answering"));
        byte response[] = "Loreto....";
        // char *xx = LnUtoa(myEEpromAddress, 3, '0');
        sendMessage(senderAddr, response, sizeof(response), pData);
    }
    else {                                // non sono io.... commento sulla seriale
        Serial.print(F("   (Request is NOT for me)"));
        rxDisplayData(0, pData);
    }
}


// #############################################################
// #
// #############################################################
void sendMessage(byte destAddr, byte data[], byte dataLen, RXTX_DATA *pData) {
    pData->tx[SENDER_ADDR]      = myEEpromAddress;    // SA
    pData->tx[DESTINATION_ADDR] = destAddr;    // DA
    pData->tx[SEQNO_HIGH]       = pData->rx[SEQNO_HIGH];    // riscrivi il seqNO
    pData->tx[SEQNO_LOW]        = pData->rx[SEQNO_LOW];    // DA

    byte index = PAYLOAD;
    for (byte i = 0; i<dataLen; i++)
        pData->tx[index++] = data[i];         // copiamo i dati nel buffer da inviare

    pData->tx[DATALEN] = index;  // set dataLen

        // send to RS-485 bus
    delay(responseDelay);
    digitalWrite(RS485_ENABLE_PIN, ENA_TX);               // enable sending
    sendMsgArduino(pData);
    digitalWrite(RS485_ENABLE_PIN, ENA_RX);                // set in receive mode
    txDisplayData(0, pData);
}

// ################################################################
// # --- DISPLAY DATA
// ################################################################

void rxDisplayData(byte rCode, RXTX_DATA *pData) {
    displayDebugMessage("inoRECV-data", rCode, pData->rx);
    displayDebugMessage("inoRECV-raw ", rCode, pData->raw);
}
void txDisplayData(byte rCode, RXTX_DATA *pData) {
    displayDebugMessage("inoSEND-data", rCode, pData->tx);
    displayDebugMessage("inoSEND-raw ", rCode, pData->raw);
}




