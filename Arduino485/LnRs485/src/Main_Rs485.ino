/*
Author:     Loreto Notarantonio
version:    LnVer_2017-11-30_19.06.39

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.
            Funzione di slave.
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/


//  /opt/arduino-1.8.1/hardware/arduino/avr/variants/standard/pins_arduino.h:#define PIN_A0   (14)
#include    <SoftwareSerial.h>
#include    <EEPROM.h>


#define     _I_AM_ARDUINO_NANO_
#define     I_AM_MAIN_

#include    <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include    <LnRS485_protocol.h>
#include    "LnRs485.h"


/*
    Per i pin di Arduino, facendo riferimento alle istruzioni di Arduino stesso, sono
    pin digitali     1, 2, 7, 8       <---- INPUT
    pin    "         10, 11, 12, 13   ----> OUTPUT
    pin   i2c        4, 5             <---> I2C
    pin analogici    A0, A1, A2, A3   <---- INPUT             controllo   !!!
    pin    "         A4, A5, A6, A7   ----> OUTPUT            controllo   !!!

    pin per la linea 485 -> 2,3,4
*/

// --------------------------------------------------------------------------------
// - simuliamo anche il ritorno in 485 sulla seriale per affinare il master python
// -     false : scrive in modalità text
// -     true  : scrive con protocollo LnRs485
// --------------------------------------------------------------------------------


//python3.4 -m serial.tools.list_ports
void setup() {


    /* --------
       INIZIALIZZAZIONE dei pin
    -------- */
    pinMode(D01, INPUT);
    // pinMode(D02, INPUT);
    // pinMode(D03, INPUT);
    // pinMode(D04, INPUT);
    // pinMode(D05, I2C);
    pinMode(D07, INPUT);
    pinMode(D08, INPUT);

    pinMode(D10, OUTPUT);
    pinMode(D11, OUTPUT);
    pinMode(D12, OUTPUT);
    pinMode(D13, OUTPUT);          // built-in LED
    /* --------
       INIZIALIZZAZIONE dei pin
    -------- */

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


}


void loopx() {
    printPINs();
}


// ################################################################
// # - M A I N     Loop
// ################################################################
void loop() {

    pData->myEEpromAddress  = myEEpromAddress;

    if (myEEpromAddress <= 10) {
        #ifdef MASTER_SIMULATOR
            if (firstRun) {
                setMyID("Emula", myEEpromAddress);
                pData->myID             = myID;
            }
            loop_MasterSimulator();
            delay(1000);

        #else
            if (firstRun) {
                setMyID("Relay", myEEpromAddress);
                pData->myID             = myID;
            }
            Relay_Main();
        #endif
    }
    else {
        if (firstRun) {
            setMyID("Slave", myEEpromAddress);
            pData->myID             = myID;
        }
        Slave_Main();

    }
    firstRun = false;

}

