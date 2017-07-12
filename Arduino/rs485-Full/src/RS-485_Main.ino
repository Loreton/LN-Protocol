/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-12_20.09.13

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
#define     I_AM_MAIN__

#define     SIMULATE_ECHOxxx
#include    <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include    <LnRS485_protocol.h>
#include    <SoftwareSerial.h>
#include    "RS-485_Full.h"                      //  pin definitions
#include    <EEPROM.h>


//python3.4 -m serial232.tools.list_ports
void setup() {

        // ===================================
        // - inizializzazione bus RS485
        // - e relativa struttura dati
        // ===================================
    Serial485.begin(9600);
    pData               = &RxTx;
    pData->displayData  = false;                // data display dei byte hex inviati e ricevuti
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
    char *xx        = LnUtoa(myEEpromAddress, 3, '0');
    // myID[0] = 13;   // CR già pre-configurati nella definizione
    // myID[1] = 10;   // NL già pre-configurati nella definizione
    myID[3] = xx[0];
    myID[4] = xx[1];
    myID[5] = xx[2];
    pData->myID = myID;

    // piSerial232.println(myID);

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

#ifdef SIMULATE_ECHO
    loop_Simulate();
#else
    if (myEEpromAddress == 1)   loop_Relay();
    else                        loop_Slave();
#endif

}



// void loop_Slave() {};
// void loop_Relay() {};
