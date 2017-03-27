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

byte fDEBUG;



byte myEEpromAddress;        // who we are

byte myAddress  = 0;
byte myAddress0 = 0;
byte myAddress1 = 0;
// byte IAM[10];
RXTX_DATA RxTx;


//python3.4 -m serial.tools.list_ports
void setup() {
    // RxTx.fDEBUG = false;
    Serial.begin(9600);             // SERIAL_8N1 (the default)
    serialRs485.begin (9600);
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);          // built-in LED

    pinMode(Addr0,  INPUT_PULLUP);  // set pullup on analog
    pinMode(Addr1,  INPUT_PULLUP);  // set pullup on analog

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



void loop() {
    RxTx.timeout = 10000;

    byte respoonse[] = "Loreto";
    sendMessage(respoonse, sizeof(respoonse), &RxTx);
    delay(2000);
}

void loop_OK0() {
    RxTx.timeout = 10000;

    byte rCode = recvMsg (fAvailable, fRead, &RxTx);

    if (rCode > 0) {
        displayErrorMessage(rCode, &RxTx);
        // displayDebugMessage(&rx);
    }
    else if (fDEBUG == true)  {
        // displayDebugMessage("[Slave] - DEBUG Richiesta ricevuta : ", &RxTx);
        displayDebugMessage("[Slave] - CMD received (DEBUG)   : ", &RxTx);
        displayRxMessage(   "[Slave] - CMD received (PAYLOAD) : ", &RxTx);
    }
    else if (RxTx.data[0] == 0) {
        Serial.print(F("\r\nNessuna richiesta ricevuta in un tempo di: "));
        Serial.print(RxTx.timeout);
        Serial.println(F("mS"));
    }
    else
        displayRxMessage("CMD received (PAYLOAD) : ", &RxTx);
        byte respoonse[] = "Loreto";
        sendMessage(respoonse, sizeof(respoonse), &RxTx);

}






// #############################################################
// #
// #############################################################
void displayErrorMessage(byte rCode, RXTX_DATA *ptr) {
    byte nBytes;
    const char *rs485ErrMsg[] = {"", " - OVERFLOW"," - BAD-CRC"," - BAD-CHAR"," - TIMEOUT"};

    Serial.print(F(" [Slave] - ERROR: "));
    Serial.print(rCode);
    Serial.println(rs485ErrMsg[rCode]);

    // display dei rawdata
    nBytes = ptr->rawData[0];
    Serial.print(F(" raw->  ("));Serial.print(nBytes);Serial.print(F(") - "));
    printHex(&ptr->rawData[1], nBytes, "\r\n"); // contiene LEN STX ...data... ETX

    // display dei data
    nBytes = ptr->data[0];
    Serial.print(F(" data-> ("));Serial.print(nBytes);Serial.print(F(") - "));
    printHex(&ptr->data[1], nBytes); // contiene solo dati


    return;
}

// #############################################################
// # const char* text : per ricevere una stringa constante es: "Loreto"
// #############################################################
void displayDebugMessage(const char* text, RXTX_DATA *pRx) {
    byte dataLen = pRx->rawData[0];

    if (dataLen > 0) {
        Serial.print(text);
        Serial.print(F("   ("));Serial.print(dataLen);Serial.print(F(") - "));
        printHex(&pRx->rawData[1], dataLen); // contiene LEN STX ...data... ETX
    }


    return;
}


// #############################################################
// #
// #############################################################
void displayRxMessage(const char* text, RXTX_DATA *pRx) {
    Serial.print(text);
    Serial.print(F("   ("));Serial.print(pRx->data[0]);Serial.print(F(") - "));
    printHex(&pRx->data[1], pRx->data[0], "\r\n");

    return;
}

// #############################################################
// #
// #############################################################
void sendMessage(byte data[], byte dataLen, RXTX_DATA *RxTx) {
    byte index = 0;

    // assemble message
    // RxTx.data[0] = dataLen+1;    // len + SA + DA
    RxTx->data[++index] = 0;    // SA
    RxTx->data[++index] = 1;    // DA

    for (byte i = 0; i<dataLen; i++)
        RxTx->data[++index] = data[i];         // copiamo i dati nel buffer da inviare

    RxTx->data[0] = --index;  // set dataLen


        // send to RS-485 bus
    digitalWrite(RS485_ENABLE_PIN, HIGH);               // enable sending
    sendMsg(fWrite, RxTx);
    digitalWrite(RS485_ENABLE_PIN, LOW);                // disable sending
    fDEBUG = true;
    if (fDEBUG)
        displayDebugMessage("[Slave] - Resp xmitted (DEBUG)  : ", RxTx);

}

