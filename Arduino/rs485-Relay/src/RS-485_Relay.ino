/*
Author:     Loreto Notarantonio
version:    LnVer_2017-05-16_10.04.04

Scope:      Funzione di relay. Prende i dati provenienti da una seriale collegata a RaspBerry
            ed inoltra il comando sul bus RS485.
            Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/

#define     _I_AM_ARDUINO_NANO_
#define     _SIMULATE_ECHO_
#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <LnRS485_protocol.h>
#include <SoftwareSerial.h>

#include "RS-485_Relay.h"                      //  pin definitions

#include <EEPROM.h>

// ------ RS485 callback routines
// void arduinofWrite(const byte what)   {       Serial485.write (what); }
// int  arduinofAvailable()              {return Serial485.available (); }
// int  arduinofRead()                   {return Serial485.read (); }

// ------ RS485 callback routines
// void pifWrite(const byte what)       {       Serial.write (what); }
// int  pifAvailable()                  {return Serial.available (); }
// int  pifRead()                       {return Serial.read (); }




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
// # - M A I N     Loop
// ################################################################
void loop() {
        // ------------------------------------
        // - riceviamo i dati da RaspBerry
        // - con protocollo LnRs485
        // ------------------------------------
    pData->timeout = 5000;
    pData->rx[DATALEN] = 0;
    byte rCode = recvMsgPi(pData);

    if (rCode == LN_OK) {
        forwardMessage(pData);
    }
}







// #############################################################
// #
// #############################################################
void forwardMessage(RXTX_DATA *pData) {
    byte dataLen = pData->rx[DATALEN];

        // - copy ALL rx to tx
    for (byte i = 0; i<=dataLen; i++)
        pData->tx[i] = pData->rx[i];         // copiamo i dati nel buffer da inviare


    // imposta sender address (Arduino Relay)
    // pData->tx[SENDER_ADDR]      = pData->rx[DESTINATION_ADDR];
    pData->tx[DESTINATION_ADDR] = pData->rx[SENDER_ADDR];
    pData->tx[SENDER_ADDR]      = myEEpromAddress;

    // printHexPDS( "ECHO_CMD : ", ECHO_CMD);
    // printHexPDS( " - RxCommand: ", pData->rx[COMMAND]);
    // Serial.println();


        // invia il messaggio indietro anche a raspBerry
    if (pData->rx[COMMAND] == ECHO_CMD) {
        sendMsgPi(pData);
    }

        // send to RS-485 bus
    digitalWrite(RS485_ENABLE_PIN, ENA_TX);               // enable sending
    sendMsgArduino(pData);
    digitalWrite(RS485_ENABLE_PIN, ENA_RX);                // set in receive mode

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













// ##########################################################
// se vogliamo che Arduino invii un echo autonomamente
// ##########################################################
void loop_simulate() {
    simulateEcho(pData);
    delay(1000);
}


// #############################################################
// # Prepariamo un pacchetto come se fosse arrivato dal Master PI
// #############################################################
// int seqNO = 0;
void simulateEcho(RXTX_DATA *pData) {
    static int seqNO = 0;

    pData->rx[SENDER_ADDR]      = 0;    // SA
    pData->rx[DESTINATION_ADDR] = myEEpromAddress;    // DA
    pData->rx[SEQNO_HIGH]       = seqNO >> 8;
    pData->rx[SEQNO_LOW]        = seqNO & 0x00FF;
    pData->rx[COMMAND]          = ECHO_CMD;


    byte data[]  = "simulated echo";
    byte dataLen = sizeof(data);
    byte index = PAYLOAD;
    for (byte i=0; i<dataLen; i++)
        pData->rx[index++] = data[i];         // copiamo i dati nel buffer da inviare

    pData->rx[DATALEN] = index;  // set dataLen

    forwardMessage(pData);

    seqNO++;

}
