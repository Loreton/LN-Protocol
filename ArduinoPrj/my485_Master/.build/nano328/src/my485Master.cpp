#include <Arduino.h>
#include <RS485_protocol.h>
#include <RS485_non_blocking.h>
#include <SoftwareSerial.h>
void fWrite(const byte what);
int  fAvailable ();
int  fRead ();
void setup();
void loop();
void LnSendMessage(const byte data);
byte LnRcvMessage(unsigned long timeOUT);
void printHex(const byte *data, const byte len);
#line 1 "src/my485Master.ino"
/*
    http://www.gammon.com.au/forum/?id=11428

*/
//#include <RS485_protocol.h>
//#include <RS485_non_blocking.h>
//#include <SoftwareSerial.h>

void printHex(const byte *data, const byte len);

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
        LnSendMessage(level);
        // if (digitalRead(START_PIN) == 1) {
        //     Serial.print("[Master] - START_PIN : ");Serial.println(digitalRead(START_PIN));
        //     break;
        // }

        if (LnRcvMessage(10000)) {
            Serial.print("[Master] - Working on response data. Sleeping for");Serial.print(SLEEP_TIME, DEC);Serial.println(" sec.");
        }

        delay(SLEEP_TIME*1000);
    }
}

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
    digitalWrite(ENABLE_PIN, HIGH);  // enable sending
    sendMsg(fWrite, msg, sizeof(msg));
    Serial.print("[Master] - Comando  inviato : ");printHex(msg, sizeof(msg));
    digitalWrite(ENABLE_PIN, LOW);  // disable sending

}


// #############################################################
// #
// #############################################################
byte LnRcvMessage(unsigned long timeOUT) {
    // receive response
    byte buf [10];

    byte rcvLen = recvMsg (fAvailable, fRead, buf, sizeof buf, timeOUT);
    digitalWrite (LED_PIN, rcvLen == 0);  // turn on LED if error

    // only send once per successful change
    if (rcvLen > 0) {
        Serial.print("[Master] - Risposta ricevuta: ");printHex(buf, rcvLen);
    } else {
        Serial.print("[Master] - TIMEOUT waiting response. len=");printHex(buf, rcvLen);
    }
    return rcvLen;
}




void printHex(const byte *data, const byte len) {
    byte i;

    Serial.print("len:");
    Serial.print(len, DEC);
    Serial.print("  -  ");
    for (i=0; i<len; i++) {
        Serial.print(data[i], HEX);
        Serial.print(" ");
    }
    Serial.println("");
}
