/*
    http://www.gammon.com.au/forum/?id=11428
*/

#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <LnRS485_protocol.h>
#include <SoftwareSerial.h>

#include "RS-485_Slave.h"                      //  pin definitions

#include <EEPROM.h>

// Author:             Loreto notarantonio
char myVersion[] = "LnVer_2017-04-07_16.49.40";

SoftwareSerial serialRs485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

// ------ callback routines
void fWrite(const byte what)   {       serialRs485.write (what); }
int  fAvailable()              {return serialRs485.available (); }
int  fRead()                   {return serialRs485.read (); }

// void fWrite(const byte what)  {Serial.write (what); }
// int fAvailable()              {return Serial.available (); }
// int fRead()                   {return Serial.read (); }



byte myEEpromAddress;        // who we are
RXTX_DATA RxTx;             // struttura dati



//python3.4 -m serial.tools.list_ports
void setup() {
    RxTx.displayData = false;    // data display dei byt hex inviatie ricevuti (lo fa direttamente la libreria)

    Serial.begin(9600);             // SERIAL_8N1 (the default)
    serialRs485.begin(9600);
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);          // built-in LED

    myEEpromAddress = EEPROM.read(0);

    delay(5*1000);

    Serial.print(F("Arduino myAddress is: "));Serial.println(LnUtoa(myEEpromAddress, 3, '0'));
    Serial.println();

}



void loop() {
    RXTX_DATA *ptr;
    ptr = &RxTx;
    ptr->timeout = 10000;
    byte rCode = recvMsg (fAvailable, fRead, &RxTx);

    if (ptr->displayData == false) {
        displayDebugMessage("inoRECV-raw ", rCode, ptr->raw);
        displayDebugMessage("inoRECV-data", rCode, ptr->rx);
    }

    if (rCode == LN_OK) {
        byte response[] = "Loreto";
        sendMessage(response, sizeof(response), &RxTx);
            // print solo se non lo ha già fatto al libreria
    }
    else if (ptr->rx[0] == 0) {
        Serial.print(F("\r\nNessuna richiesta ricevuta in un tempo di: "));
        Serial.print(ptr->timeout);
        Serial.println(F("mS"));
    }

}

#if 0
// #############################################################
// #
// #############################################################
void processRequest(RXTX_DATA *ptr) {


    ptr->tx[++index] = myEEpromAddress;    // SA
    ptr->tx[++index] = 0;    // DA

    for (byte i = 0; i<dataLen; i++)
        ptr->tx[++index] = data[i];         // copiamo i dati nel buffer da inviare

    ptr->tx[0] = --index;  // set dataLen

        // send to RS-485 bus
    digitalWrite(RS485_ENABLE_PIN, HIGH);               // enable sending
    sendMsg(fWrite, RxTx);
    digitalWrite(RS485_ENABLE_PIN, LOW);                // disable sending

    Serial.println();
}
#endif

// #############################################################
// #
// #############################################################
void sendMessage(byte data[], byte dataLen, RXTX_DATA *ptr) {
    // RXTX_DATA *ptr;
    // ptr = &RxTx;

    byte index = 0;

    ptr->tx[++index] = myEEpromAddress;    // SA
    ptr->tx[++index] = 0;    // DA

    for (byte i = 0; i<dataLen; i++)
        ptr->tx[++index] = data[i];         // copiamo i dati nel buffer da inviare

    ptr->tx[0] = --index;  // set dataLen

        // send to RS-485 bus
    digitalWrite(RS485_ENABLE_PIN, HIGH);               // enable sending
    sendMsg(fWrite, ptr);
    digitalWrite(RS485_ENABLE_PIN, LOW);                // disable sending

    // --- DISPLAY DATA
    if (ptr->displayData == false) {
        displayDebugMessage("inoSEND-data", LN_OK, ptr->tx);
        displayDebugMessage("inoSEND-raw ", LN_OK, ptr->raw);
    }

    Serial.println();
}


#if 0
void loop() {
    ptr->timeout = 10000;
    const char LN_RECV_CALLER[] = "inoRECV";

    byte rCode = recvMsg (fAvailable, fRead, &RxTx);


    if (rCode > 0) {
        displayDebugMessage(LN_RECV_CALLER, rCode, ptr->raw);
    }
    else if (fDEBUG == true)  {
        displayDebugMessage(LN_RECV_CALLER, rCode, ptr->raw);
        displayDebugMessage(LN_RECV_CALLER, rCode, ptr->data);
    }
    else if (ptr->data[0] == 0) {
        Serial.print(F("\r\nNessuna richiesta ricevuta in un tempo di: "));
        Serial.print(ptr->timeout);
        Serial.println(F("mS"));
    }
    else
        displayDebugMessage(LN_RECV_CALLER, rCode, ptr->data);
        byte response[] = "Loreto";
        sendMessage(response, sizeof(response), &RxTx);
}



void printName(void) {
    Serial.print(F("[addr:"));Serial.print(myEEpromAddress);Serial.print(F("] - "));
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


void loop_SEND() {
    ptr->timeout = 10000;

    byte response[] = "Loreto";
    sendMessage(response, sizeof(response), &RxTx);
    delay(2000);
}

#endif