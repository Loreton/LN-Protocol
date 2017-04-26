/*
    http://www.gammon.com.au/forum/?id=11428
*/

#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <LnRS485_protocol.h>
#include <SoftwareSerial.h>

#include "RS-485_Slave.h"                      //  pin definitions

#include <EEPROM.h>

// Author:             Loreto notarantonio
char myVersion[] = "LnVer_2017-04-26_11.35.24";

SoftwareSerial serialRs485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

// ------ callback routines
void fWrite(const byte what)   {       serialRs485.write (what); }
int  fAvailable()              {return serialRs485.available (); }
int  fRead()                   {return serialRs485.read (); }

// void fWrite(const byte what)  {Serial.write (what); }
// int fAvailable()              {return Serial.available (); }
// int fRead()                   {return Serial.read (); }

#define DATALEN     0
#define SENDER      1
#define DESTINATION 2
#define PAYLOAD     3
#define ENA_TX       HIGH
#define ENA_RX       LOW

byte        myEEpromAddress;        // who we are
RXTX_DATA   RxTx, *pData;             // struttura dati
//.............01234567890123
char myID[] = "[xxx] - ";
unsigned long responseDelay = 0;



//python3.4 -m serial.tools.list_ports
void setup() {
    pData      = &RxTx;

    pData->displayData = true;    // data display dei byt hex inviatie ricevuti (lo fa direttamente la libreria)

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
    myID[1] = xx[0];
    myID[2] = xx[1];
    myID[3] = xx[2];
    pData->myID = myID;

    // delay(5*1000);

    Serial.println(myID);
    if (myEEpromAddress == 11)
        responseDelay = 1000;
    if (myEEpromAddress == 12)
        responseDelay = 4000;

}


// ################################################################
// #
// ################################################################
void loop() {
    // RXTX_DATA *pData;
    // pData = &RxTx;
    pData->timeout = 10000;
    byte rCode = recvMsg (fAvailable, fRead, pData);

    // displayData(rCode, pData)
    if (rCode == LN_OK) {
        processRequest(pData);
    }

    else if (pData->rx[0] == 0) {
        Serial.print(myID);
        Serial.print(F("rCode: "));Serial.print(rCode);
        Serial.print(F(" - Nessuna richiesta ricevuta in un tempo di: "));
        Serial.print(pData->timeout);
        Serial.println(F("mS"));
    }

}

// #############################################################
// #
// #############################################################
void processRequest(RXTX_DATA *pData) {
    // byte dataLen    = pData->rx[DATALEN];
    byte senderAddr = pData->rx[SENDER];
    byte destAddr   = pData->rx[DESTINATION];

    Serial.print(myID); Serial.print(F("from: ")); Serial.print(senderAddr);
                        Serial.print(F(" to  : ")); Serial.print(destAddr);

    if (destAddr == myEEpromAddress) {    // sono io.... rispondi sulla RS485
        Serial.println(F("   (Request is for me)"));
        Serial.println();
        Serial.print(myID); Serial.println(F("answering..."));
        byte response[] = "Loreto";
        sendMessage(senderAddr, response, sizeof(response), pData);
    }
    else {                                // non sono io.... commento sulla seriale
        Serial.println(F("   (Request is NOT for me)"));
        Serial.println();
        rxDisplayData(0, pData);
    }
}


// #############################################################
// #
// #############################################################
void sendMessage(byte destAddr, byte data[], byte dataLen, RXTX_DATA *pData) {
    pData->tx[SENDER]       = myEEpromAddress;    // SA
    pData->tx[DESTINATION]  = destAddr;    // DA

    byte index = PAYLOAD;
    for (byte i = 0; i<dataLen; i++)
        pData->tx[index++] = data[i];         // copiamo i dati nel buffer da inviare

    pData->tx[DATALEN] = index;  // set dataLen

        // send to RS-485 bus
    delay(responseDelay);
    digitalWrite(RS485_ENABLE_PIN, ENA_TX);               // enable sending
    sendMsg(fWrite, pData);
    digitalWrite(RS485_ENABLE_PIN, ENA_RX);                // set in receive mode
}

// ################################################################
// # --- DISPLAY DATA
// ################################################################

void rxDisplayData(byte rCode, RXTX_DATA *pData) {
    displayDebugMessage("inoRECV-data", rCode, pData->rx);
    displayDebugMessage("inoSEND-raw ", rCode, pData->raw);
}
void txDisplayData(byte rCode, RXTX_DATA *pData) {
    displayDebugMessage("inoSEND-data", rCode, pData->tx);
    displayDebugMessage("inoSEND-raw ", rCode, pData->raw);
}



// void LnPrint(byte *text) {
//     Serial.print(myID);
//     Serial.print(text)
// }


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

