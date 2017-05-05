/*
    http://www.gammon.com.au/forum/?id=11428
*/

#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <LnRS485_protocol.h>
#include <SoftwareSerial.h>

#include "RS-485_Slave.h"                      //  pin definitions

#include <EEPROM.h>

// Author:             Loreto notarantonio
char myVersion[] = "LnVer_2017-05-05_15.19.42";

SoftwareSerial serialRs485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

// ------ callback routines
void fWrite(const byte what)   {       serialRs485.write (what); }
int  fAvailable()              {return serialRs485.available (); }
int  fRead()                   {return serialRs485.read (); }

// void fWrite(const byte what)  {Serial.write (what); }
// int fAvailable()              {return Serial.available (); }
// int fRead()                   {return Serial.read (); }

// #define DATALEN     0
// #define SENDER_ADDR      1
// #define DESTINATION_ADDR 2
// #define SEQNO_HIGH    3
// #define SEQNO_LOW     4
// #define PAYLOAD     5
#define ENA_TX       HIGH
#define ENA_RX       LOW
#define DIS_TX       LOW

byte        myEEpromAddress;        // who we are
RXTX_DATA   RxTx, *pData;             // struttura dati
//.............01234567890123
char myID[] = "rn[xxx] - ";
unsigned long responseDelay = 0;



//python3.4 -m serial.tools.list_ports
void setup() {
    pData      = &RxTx;

    pData->displayData = false;    // data display dei byt hex inviatie ricevuti (lo fa direttamente la libreria)

    Serial.begin(9600);             // SERIAL_8N1 (the default)
    serialRs485.begin(9600);
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // enable rx by default
    digitalWrite(RS485_ENABLE_PIN, ENA_RX);  // set in receive mode

    pinMode (LED_PIN, OUTPUT);          // built-in LED

    /* ------------------------
        preparazione myID con indirizzo
        1. convert integer myAddress to string
        2. copy string into myID array
    */
    myEEpromAddress = EEPROM.read(0);
    char *xx = LnUtoa(myEEpromAddress, 3, '0');
    myID[0] = 13;   // CR
    myID[1] = 10;   // NL
    myID[3] = xx[0];
    myID[4] = xx[1];
    myID[5] = xx[2];
    pData->myID = myID;

    // delay(5*1000);

    Serial.println(myID);

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

}


// ################################################################
// #
// ################################################################
void loop() {
    pData->timeout = 10000;
    byte rCode = recvMsg (fAvailable, fRead, pData);

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
                        Serial.print(F(" [")); Serial.print(seqNO);Serial.print(F("]"));

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
    sendMsg(fWrite, pData);
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



/*
Configurazione

rs485_01 - pennetta
rs485_02 - pennetta
rs485_03 - pennetta

arduino11 - Arduino nano
arduino12 - Arduino nano

rs485_01 - trasmette sia per arduino11 che per arduino12


rs485_01        rs482_02        arduino11         - arduino12

send->11        -               -                   -
-               00-->11         -                   -
-               -               OK                   -
-               -               00<--reply           -
-               00<--11         -                   -
-               -                 -                   -
-               -                 -                   -
-               -                 -                   -
-               -                 -                   -

*/

