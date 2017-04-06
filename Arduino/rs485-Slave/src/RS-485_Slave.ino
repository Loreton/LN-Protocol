/*
    http://www.gammon.com.au/forum/?id=11428
*/

#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
#include <LnRS485_protocol.h>
#include <SoftwareSerial.h>

#include "RS-485_Slave.h"                      //  pin definitions

#include <EEPROM.h>

// Author:             Loreto notarantonio
char myVersion[] = "LnVer_2017-04-05_14.31.08";

SoftwareSerial serialRs485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

// callback routines
void fWrite(const byte what)   {       serialRs485.write (what); }
int  fAvailable()              {return serialRs485.available (); }
int  fRead()                   {return serialRs485.read (); }

// void fWrite(const byte what)  {Serial.write (what); }
// int fAvailable()              {return Serial.available (); }
// int fRead()                   {return Serial.read (); }


byte fDEBUG = false;

byte myEEpromAddress;        // who we are

byte myAddress  = 0;
byte myAddress0 = 0;
byte myAddress1 = 0;
RXTX_DATA RxTx;


//python3.4 -m serial.tools.list_ports
void setup() {
    RxTx.displayData = true;

    Serial.begin(9600);             // SERIAL_8N1 (the default)
    serialRs485.begin(9600);
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);          // built-in LED

    pinMode(Addr0,  INPUT_PULLUP);  // set pullup on analog
    pinMode(Addr1,  INPUT_PULLUP);  // set pullup on analog

    myEEpromAddress = EEPROM.read(0);

    delay(5*1000);

    // loop_DisplayAddress();
    Serial.print(F("this Version   : "));Serial.println(myVersion);
    Serial.print(F("EEprom Address : "));Serial.println(myEEpromAddress);

}


void loop() {
    RxTx.timeout = 10000;

    byte rCode = recvMsg (fAvailable, fRead, &RxTx);

    if (rCode > 0) {
        displayDebugMessage(rCode, RxTx.rawData);
    }
    else if (fDEBUG == true)  {
        displayDebugMessage(rCode, RxTx.rawData);
        displayDebugMessage(rCode, RxTx.data);
    }
    else if (RxTx.data[0] == 0) {
        Serial.print(F("\r\nNessuna richiesta ricevuta in un tempo di: "));
        Serial.print(RxTx.timeout);
        Serial.println(F("mS"));
    }
    else
        displayDebugMessage(rCode, RxTx.data);
        byte respoonse[] = "Loreto";
        sendMessage(respoonse, sizeof(respoonse), &RxTx);

}



void printName(void) {
    Serial.print(F("[addr:"));Serial.print(myEEpromAddress);Serial.print(F("] - "));
}





// #############################################################
// #
// #############################################################
void sendMessage(byte data[], byte dataLen, RXTX_DATA *RxTx) {
    byte index = 0;

    // assemble message
    // RxTx.data[0] = dataLen+1;    // len + SA + DA
    RxTx->data[++index] = myEEpromAddress;    // SA
    RxTx->data[++index] = 0;    // DA

    for (byte i = 0; i<dataLen; i++)
        RxTx->data[++index] = data[i];         // copiamo i dati nel buffer da inviare

    RxTx->data[0] = --index;  // set dataLen


        // send to RS-485 bus
    digitalWrite(RS485_ENABLE_PIN, HIGH);               // enable sending
    sendMsg(fWrite, RxTx);
    digitalWrite(RS485_ENABLE_PIN, LOW);                // disable sending

    if (fDEBUG)
        displayDebugMessage(LN_DEBUG, RxTx->rawData);
    else
        displayDebugMessage(LN_PAYLOAD, RxTx->data);

    Serial.println();
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
    RxTx.timeout = 10000;

    byte respoonse[] = "Loreto";
    sendMessage(respoonse, sizeof(respoonse), &RxTx);
    delay(2000);
}

