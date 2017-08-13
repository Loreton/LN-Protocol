/*
Author:     Loreto Notarantonio
version:    LnVer_2017-08-13_16.33.21

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.
            Funzione di slave.
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/

#define     _I_AM_ARDUINO_NANO_
#define     I_AM_MAIN_

#define     POLLING_SIMULATION
#include    <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include    <EEPROM.h>


#include    <LnRS485_protocol.h>
#include    <SoftwareSerial.h>
#include    "RS-485_Full.h"                      //  pin definitions





//python3.4 -m serial.tools.list_ports
void setup() {

        // ===================================
        // - inizializzazione bus RS485
        // - e relativa struttura dati
        // ===================================
    Serial485.begin(9600);
    pData = &RxTx;

    pinMode(RS485_ENABLE_PIN, OUTPUT);          // enable rx by default
    digitalWrite(RS485_ENABLE_PIN, ENA_485_RX);     // set in receive mode

        // ===================================
        // - inizializzazione porta seriale
        // - di comunicazione con raspBerry
        // ===================================
    Serial232.begin(9600);             // default 8N1 - Serial renamed to Serial232 in .h

        // ================================================
        // - Preparazione myID con indirizzo di Arduino
        // -    1. convert integer myAddress to string
        // -    2. copy string into myID array
        // ================================================
    myEEpromAddress = EEPROM.read(0);

    // Serial.print(myID); altrimenti scrive anche sul relay ee è meglio evitare rumore.

    pinMode (LED_PIN, OUTPUT);          // built-in LED

}




// ################################################################
// # - M A I N     Loop
// ################################################################
void loop() {
    if (myEEpromAddress <= 10) {
        #ifdef POLLING_SIMULATION
            if (firstRun) {
                setMyID("Emula", myEEpromAddress);
                pData->myID = myID;
            }
            loop_PollingSimulation();
            delay(1000);

        #else
            if (firstRun) {
                setMyID("Relay", myEEpromAddress);
                pData->myID = myID;
            }
            rs485_Relay();
        #endif
    }
    else {
        if (firstRun) {
            setMyID("Slave",myEEpromAddress);
            pData->myID = myID;
        }
        loop_Slave();

    }
    firstRun = false;

}



