/*
    http://www.gammon.com.au/forum/?id=11428

*/
#include <LnFunctions.h>                //  D2X(dest, val, 2), printHex
// #include <RS485_protocol.h>
#include <LnRS485_non_blocking.h>
#include <SoftwareSerial.h>

#include "RS-485_Slave.h"                      //  pin definitions




SoftwareSerial RS485 (RS485_RX_PIN, RS485_TX_PIN);  // receive pin, transmit pin

// callback routines
void fWrite(const byte what) {RS485.write (what); }
int  fAvailable ()          {return RS485.available (); }
int  fRead ()               {return RS485.read (); }


/* --------------------
    mi serve per verificare i dati e l'ordine con cui sono
    stati inviati inclusi STX, CRC, ETX
    DEBUG_TxRxMsg[0] contiene lunghezza dei dati
-------------------- */
byte DEBUG_TxRxMsg [200] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC
byte rxData         [60];

byte myAddress = 0;
byte myAddress0 = 0;
byte myAddress1 = 0;


//python3.4 -m serial.tools.list_ports
void setup() {
    Serial.begin(9600);
    RS485.begin (9600);
    pinMode (RS485_ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);          // built-in LED

    pinMode(Addr0,  INPUT_PULLUP);  // set pullup on analog
    pinMode(Addr1,  INPUT_PULLUP);  // set pullup on analog
    // pinMode(Addr0,  INPUT);  // set pullup on analog
    // pinMode(Addr1,  INPUT);  // set pullup on analog
}



void loop_() {
    myAddress0 = digitalRead(Addr0);
    Serial.print("Porta Addr0: ");       Serial.println(myAddress0);

    myAddress1 = digitalRead(Addr1);
    Serial.print("Porta Addr1: ");       Serial.println(myAddress1);

    byte value0 = 0.5 + pow(2, 0);
    byte value1 = 0.5 + pow(2, 1);
    myAddress = myAddress1*value1 + myAddress0*value0;
    Serial.print("Indirizzo di porta: ");Serial.println(myAddress);
    Serial.println("");
    delay(5*1000);

}

void loop() {
    byte SLEEP_TIME=10;
    byte level = 0;
    int timeOut = 10000;

    for (level=0; level<=255; level++) {
        // Serial.println("");

        if (readMessage(timeOut)) {
            // Serial.print("\r\n[Slave] - Working on response data. Sleeping for ");
            // Serial.print(SLEEP_TIME, DEC);
        }
        else {
            Serial.print("Nessuna risposta ricevuta in un tempo di: ");
            Serial.print(timeOut);
            Serial.println("mS");
        }
    }
}





// bool fDEBUG             = false;
bool fDEBUG             = true;

// #############################################################
// #
// #############################################################
byte readMessage(unsigned long timeOUT) {
    // receive response

    byte rxDataLen = recvMsg (fAvailable, fRead, rxData, sizeof(rxData), timeOUT, DEBUG_TxRxMsg);

    if (fDEBUG) { // print del buffer di DEBUG con tutti i dati ricevuti
        if (DEBUG_TxRxMsg[0] > 0) {
            Serial.println("\r\n[Slave] - DEBUG Risposta ricevuta : ");
            Serial.print("   ");
            Serial.print("(");Serial.print(DEBUG_TxRxMsg[0]);Serial.print(") - ");
            printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxMsg[0], ""); // contiene LEN STX ...data... ETX
        }
    }

    else {
        // only send once per successful change
        if (rxDataLen > 0) {
            Serial.print("\r\n[Slave] - Risposta ricevuta       : ");
            printHex(rxData, rxDataLen, "");
        } else {
            Serial.print("\r\n[Slave] - TIMEOUT waiting response. len=");
            printHex(rxData, rxDataLen, "");
        }
    }
    return rxDataLen;
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
    sendMsg(fWrite, txData, sizeof(txData), DEBUG_TxRxMsg);
    digitalWrite(RS485_ENABLE_PIN, LOW);                // disable sending

    if (fDEBUG) {
        // char DEBUG_SentMsgLen = *DEBUG_sentMsg;           // byte 0
        char DEBUG_TxRxLen = *DEBUG_TxRxMsg;           // byte 0
        // Serial.print("\r\n[Master] - Comando  inviato : ");printHex(&DEBUG_sentMsg[1], DEBUG_SentMsgLen, "[STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
        Serial.print("\r\n[Master] - DEBUG Comando  inviato  : ");
        printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
    }
    else {
        Serial.print("\r\n[Master] - Comando  inviato        : ");printHex(txData, txDataLen, "");
    }

}

