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
// byte IAM[10];
RXTX_DATA rx;

//python3.4 -m serial.tools.list_ports
void setup() {
    rx.fDEBUG = false;
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

    // String IAM = String("Loreto") + String(myEEpromAddress); // occupa 1600 bytes circa
    // sprintf(IAM, "%s%d", "Slave", myEEpromAddress);
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


void loop() {
    rx.timeout = 10000;

    byte rCode = recvMsg (fAvailable, fRead, &rx);

    if (rCode > 0) {
        displayErrorMessage(rCode, &rx);
        displayDebugMessage(&rx);
        rx.fDEBUG=true;                     // varrà per il prossimo giro
    }
    else if (rx.fDEBUG == true)  {
        displayDebugMessage(&rx);
        displayRxMessage(&rx);
    }
    else if (rx.dataCounter == 0) {
        Serial.print(F("\r\nNessuna risposta ricevuta in un tempo di: "));
        Serial.print(rx.timeout);
        Serial.println(F("mS"));
    }
    else
        displayRxMessage(&rx);

}






// #############################################################
// #
// #############################################################
void displayErrorMessage(byte rCode, RXTX_DATA *ptr) {
    const char *rs485ErrMsg[] = {"", " - OVERFLOW"," - BAD-CRC"," - BAD-CHAR"," - TIMEOUT"};
    Serial.print(F("\r\n[Slave] - ERROR: "));
    Serial.print(ptr->rCode);
    Serial.println(rs485ErrMsg[rCode]);
    // Serial.println(rs485ErrMsg[rCode]);
    return;
}

// #############################################################
// #
// #############################################################
void displayDebugMessage(RXTX_DATA *pRx) {

    if (pRx->rawCounter > 0) {
        Serial.println(F("\r\n[Slave] - DEBUG Risposta ricevuta : "));
        Serial.print(F("   "));
        Serial.print(F("("));Serial.print(pRx->rawCounter);Serial.print(F(") - "));
        printHex(pRx->rawData, pRx->rawCounter, ""); // contiene LEN STX ...data... ETX
    }


    return;
}


// #############################################################
// #
// #############################################################
void displayRxMessage(RXTX_DATA *pRx) {

    // only send once per successful change
    Serial.print(F("\r\n[Slave] - Risposta ricevuta       : "));
    printHex(pRx->data, pRx->dataCounter, "");

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

