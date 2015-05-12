/*
    http://www.gammon.com.au/forum/?id=11428

*/
#include <LnFunctions.h>                //  D2X(dest, val, 2)
#include <RS485_protocol.h>
#include <RS485_non_blocking.h>
#include <SoftwareSerial.h>

// void printHex(const byte *data, const byte len, char * endStr);

#define START_PIN       5
#define ENABLE_PIN      3
#define RX_PIN         10
#define TX_PIN         11
#define LED_PIN        13



SoftwareSerial RS485 (RX_PIN, TX_PIN);  // receive pin, transmit pin

// callback routines
void fWrite(const byte what) {
    RS485.write (what);
}
int  fAvailable () {
    return RS485.available ();
}
int  fRead () {
    return RS485.read ();
}



void setup() {
    Serial.begin(9600);
    RS485.begin (9600);
    pinMode (START_PIN, INPUT);
    pinMode (ENABLE_PIN, OUTPUT);  // driver output enable
    pinMode (LED_PIN, OUTPUT);  // built-in LED
}  // end of setup



void loop() {
    byte SLEEP_TIME=10;
    byte level = 0;
    for (level=0; level<=255; level++) {
        Serial.println("");
        LnSendMessage(level);
        // if (digitalRead(START_PIN) == 1) {
        //     Serial.print("\r\n[Master] - START_PIN : ");Serial.println(digitalRead(START));
        //     break;
        // }

        if (LnRcvMessage(10000)) {
            Serial.print("\r\n[Master] - Working on response data. Sleeping for ");Serial.print(SLEEP_TIME, DEC);Serial.println("");
        }
        delay(SLEEP_TIME*1000);
    }
}


bool fDEBUG = true;
/* --------------------
    mi serve per verificare i dati e l'ordine con cui sono
    stati inviati inclusi STX, CRC, ETX
    DEBUG_sentMsg[0] contiene lunghezza dei dati
-------------------- */
byte DEBUG_TxRxMsg [200] = "                                                                ";   // gli faccio scrivere il messaggio inviato con relativo CRC


// DEV=/dev/Arduino1 && ino build -m nano328 && ino upload -p $DEV -m nano328 && ino serial -p $DEV
// #############################################################
// #
// #############################################################
void LnSendMessage(const byte data) {
    // assemble message
    byte msg [] = {
                1,    // device 1
                2,    // turn light on
                data
            };


        // send to slave
    char msgLen = sizeof(msg);
    digitalWrite(ENABLE_PIN, HIGH);  // enable sending
    sendMsg(fWrite, msg, sizeof(msg), DEBUG_TxRxMsg);
    digitalWrite(ENABLE_PIN, LOW);  // disable sending

    if (fDEBUG) {
        // char DEBUG_SentMsgLen = *DEBUG_sentMsg;           // byte 0
        char DEBUG_TxRxLen = *DEBUG_TxRxMsg;           // byte 0
        // Serial.print("\r\n[Master] - Comando  inviato : ");printHex(&DEBUG_sentMsg[1], DEBUG_SentMsgLen, "[STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
        Serial.print("\r\n[Master] - DEBUG Comando  inviato  : ");printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
    }
    else {
        Serial.print("\r\n[Master] - Comando  inviato        : ");printHex(msg, msgLen, "");
    }

}


// #############################################################
// #
// #############################################################
byte LnRcvMessage(unsigned long timeOUT) {
    // receive response
    byte buf [10];

    byte rcvLen = recvMsg (fAvailable, fRead, buf, sizeof buf, timeOUT, DEBUG_TxRxMsg);
    digitalWrite (LED_PIN, rcvLen == 0);  // turn on LED if error


    if (fDEBUG) {
        // char DEBUG_SentMsgLen = *DEBUG_sentMsg;           // byte 0
        char DEBUG_TxRxLen = *DEBUG_TxRxMsg;           // byte 0
        // Serial.print("\r\n[Master] - Comando  inviato : ");printHex(&DEBUG_sentMsg[1], DEBUG_SentMsgLen, "[STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
        Serial.print("\r\n[Master] - DEBUG Risposta ricevuta : ");printHex(&DEBUG_TxRxMsg[1], DEBUG_TxRxLen, " - [STX ...data... CRC ETX]"); // contiene LEN STX ...data... ETX
    }

    // only send once per successful change
    if (rcvLen > 0) {
        Serial.print("\r\n[Master] - Risposta ricevuta       : ");printHex(buf, rcvLen, "");
    } else {
        Serial.print("\r\n[Master] - TIMEOUT waiting response. len=");printHex(buf, rcvLen, "");
    }
    return rcvLen;
}


// char *D2X(unsigned int Valore, char size);

#if 0
void printHex(const byte *data, const byte len, char * endStr) {
    byte i;

    Serial.print("len:");
    Serial.print(len, DEC);
    Serial.print("  -  ");
    char *buff = "0000000000";
    for (i=0; i<len; i++) {
        D2X(buff, data[i], 2);
        Serial.print(buff);
        Serial.print(" ");
    }
    Serial.println(endStr);
}
#endif

