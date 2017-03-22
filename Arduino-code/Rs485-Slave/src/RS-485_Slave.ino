/*
    http://www.gammon.com.au/forum/?id=11428

*/
#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <LnRS485_protocol.h>
// #include <LnRS485_non_blocking.h>
#include <SoftwareSerial.h>

#include "RS-485_Slave.h"                      //  pin definitions

#include <EEPROM.h>

char myVersion[] = "2017-03-20 07.45.44";

SoftwareSerial serialRs485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

// callback routines
void fWrite(const byte what)   {       serialRs485.write (what); }
int  fAvailable()              {return serialRs485.available (); }
int  fRead()                   {return serialRs485.read (); }

// void fWrite(const byte what)  {Serial.write (what); }
// int fAvailable()              {return Serial.available (); }
// int fRead()                   {return Serial.read (); }





/* --------------------
    mi serve per verificare i dati e l'ordine con cui sono
    stati inviati inclusi STX, CRC, ETX

    DEBUG_data[]    contiene row data
    DEBUG_data[0]   contiene lunghezza dei dati, 255 per disabilitare il DEBUG
-------------------- */

// byte DEBUG_data [200] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC
#define MAX_MSG_SIZE            50
#define MAX_DEBUG_SIZE          2       // 2*MAX_MSG_SIZE per abilitarlo oppure limitarlo a 2

byte rxData[MAX_MSG_SIZE];
byte DEBUG_data[MAX_DEBUG_SIZE];
byte fDEBUG;



byte myEEpromAddress;        // who we are

byte myAddress  = 0;
byte myAddress0 = 0;
byte myAddress1 = 0;

//python3.4 -m serial.tools.list_ports
void setup() {
    DEBUG_data[0] = 255;
    if (DEBUG_data[0] == 255)
        fDEBUG = false;
    else
        fDEBUG = true;


    Serial.begin(9600);             // SERIAL_8N1 (the default)
    serialRs485.begin (9600);
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);          // built-in LED

    pinMode(Addr0,  INPUT_PULLUP);  // set pullup on analog
    pinMode(Addr1,  INPUT_PULLUP);  // set pullup on analog
    // pinMode(Addr0,  INPUT);  // set pullup on analog
    // pinMode(Addr1,  INPUT);  // set pullup on analog

    myEEpromAddress = EEPROM.read (0);
    delay(5*1000);

    // loop_DisplayAddress();
    Serial.print(F("this Version   : "));Serial.println(myVersion);
    Serial.print(F("EEprom Address : "));Serial.println(myEEpromAddress);

}



void loop_DisplayAddress() {
    myAddress0 = digitalRead(Addr0);
    Serial.print(F("Porta Addr0: "));       Serial.println(myAddress0);

    myAddress1 = digitalRead(Addr1);
    Serial.print(F("Porta Addr1: "));       Serial.println(myAddress1);


    byte value0 = 0.5 + pow(2, 0);
    byte value1 = 0.5 + pow(2, 1);
    myAddress = myAddress1*value1 + myAddress0*value0;
    Serial.print(F("Indirizzo di porta: "));Serial.println(myAddress);
    Serial.println("");

}

void loop_AAA() {

    while(!serialRs485.available());
    while (serialRs485.available() > 0) {
        byte inByte = serialRs485.read();
        printHexPDS("received: ", inByte);
        delay(1);
    }
}

RXTX_DATA rx;

void loop() {
    // byte SLEEP_TIME =10;
    byte level      = 0;
    int timeOut     = 10000;

    rx.sourceAddress = 0;
    rx.destAddress = 0;
    rx.fDEBUG = false;
    // rx.buffLen = sizeof(rx.data);
    rx.timeout = 10000;

    for (level=0; level<=255; level++) {
        // byte rxDataLen = recvMsg (fAvailable, fRead, rxData, sizeof(rxData), timeOut, DEBUG_data);
        byte rxDataLen = recvMsg (fAvailable, fRead, &rx);

        processDebugMessage();
        if (rxDataLen) {
            processRxMessage(rxDataLen);
        }
        else {
            Serial.print(F("Nessuna risposta ricevuta in un tempo di: "));
            Serial.print(timeOut);
            Serial.println(F("mS"));
        }
    }
}





// bool fDEBUG             = false;

// #############################################################
// #
// #############################################################
void processDebugMessage() {

    if (fDEBUG) {

        if (rx.debugData[0] > 0) {
            Serial.println(F("\r\n[Slave] - DEBUG Risposta ricevuta : "));
            Serial.print(F("   "));
            Serial.print(F("("));Serial.print(rx.debugData[0]);Serial.print(F(") - "));
            printHex(&rx.debugData[1], rx.debugData[0], ""); // contiene LEN STX ...data... ETX
        }
    }

    return;
}


// #############################################################
// #
// #############################################################
void processRxMessage(byte rxDataLen) {

    // only send once per successful change
    Serial.print(F("\r\n[Slave] - Risposta ricevuta       : "));
    printHex(rx.data, rxDataLen, "");

    // we cannot receive a message from ourself
    // someone must have given two devices the same address
    // if (RXTX_DATA.sourceAddress == myEEpromAddress) {
    //     digitalWrite (ERROR_PIN, HIGH);
    //     Serial.print(F("\r\n[Slave] - messaggio inviato con il mio sourceAddress"));
    // }  // can't receive our address


    return;
}

// #############################################################
// #
// #############################################################
void sendMessage(const byte data) {

    // assemble message
    byte txData [] = {
                1,    // device 1
                2,    // turn light on
                data
            };


        // send to RS-485 bus
    char txDataLen = sizeof(txData);
    digitalWrite(RS485_ENABLE_PIN, HIGH);               // enable sending
    sendMsg(fWrite, txData, sizeof(txData), DEBUG_data);
    digitalWrite(RS485_ENABLE_PIN, LOW);                // disable sending

    if (fDEBUG) {
        // char DEBUG_SentMsgLen = *DEBUG_sentMsg;           // byte 0
        char DEBUG_TxRxLen = *DEBUG_data;           // byte 0
        // Serial.print(F("\r\n[Master] - Comando  inviato : ");printHex(&DEBUG_sentMsg[1], DEBUG_SentMsgLen, "[STX ...data... CRC ETX]"); // contiene LEN STX ...data... ET)X
        Serial.print(F("\r\n[Master] - DEBUG Comando  inviato  : "));
        printHex(&DEBUG_data[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
    }
    else {
        Serial.print(F("\r\n[Master] - Comando  inviato        : "));printHex(txData, txDataLen, "");
    }

}

