#include <Arduino.h>
#include "LnProtocolSlave.h"
#include "SlaveAddress.h"
void setup();
void loop();
void printMsg(byte *data, byte len);
uint8_t chekForRequest();
void sendResponse(int DELAY, byte *msg, byte len);
#line 1 "src/LnProtocolSlave.ino"
/* FILE:    MXFS03V_433MHZ_MODULE_HCMODU0007_TRANSMIT_EXAMPLE
   DATE:    O8/10/2015
   VERSION: 0.1
   AUTHOR:  Loreto Notarantonio

FROM:   http://forum.hobbycomponents.com/viewtopic.php?f=25&t=1324

This is an example of how to use the 433MHz wireless transmitter module
(HCMODU0007) which is the Tx part of the tranmitter and receiver module pair.
This example makes use of the VirtualWire library written by Mike McCauley.
The sketch will read a value from the analogue input A0 and transmit it as
2 bytes to the receiver module once every second.

Tx MODULE CONNECTIONS:

PIN  DESCRIPTION      ARDUINO PIN
1    GND              GND
2    VCC (3.5-12V)    VCC
3    TX DATA          D2


You may copy, alter and reuse this code in any way you like, but please leave
reference to HobbyComponents.com in your comments if you redistribute this code.

THIS SOFTWARE IS PROVIDED "AS IS". HOBBY COMPONENTS LTD MAKES NO WARRANTIES, WHETHER
EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ACCURACY OR LACK OF NEGLIGENCE.
HOBBY COMPONENTS SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR ANY DAMAGES,
INCLUDING, BUT NOT LIMITED TO, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES FOR ANY
REASON WHATSOEVER.
*/


#define _I_AM_MAIN_

//#include "LnProtocolSlave.h"
//#include "SlaveAddress.h"



// byte RxBufferSize   =   100;
// byte TxBufferSize   =   100;
byte RxMsg[RX_BUFFERSIZE];
byte TxMsg[TX_BUFFERSIZE];

bool fDEBUG = false;

void setup() {
    Serial.begin(9600);   // Debugging only
    Serial.println("setup");

    deviceName[255] = "BROADCAST";

    // for (int i=0; i<NumberOfDevices; i++)
    //   Serial.println(deviceName[i]);



        // Initialises the TX - RX pin used to send data to the Tx module
    vw_set_tx_pin(TX_433MHz_Pin);
    vw_set_rx_pin(RX_433MHz_Pin);

    #if defined DR3100
        const int   TX_433MHz_Enable_pin     = D10;   // D9 - Default D10
        // Required for DR3100 - Set the transmit logic level (LOW = transmit for this version of module)
        // Loreto: I miei moduli non hanno il pin di ENA
        vw_set_ptt_inverted(true);
        vw_set_ptt_pin(TX_433MHz_Enable_pin);
    #endif

    vw_setup(BITS_PER_SEC);
    vw_rx_start();                      // Start the receiver PLL running

    pinMode(LED, OUTPUT);
}


//#####################################################
//# - Main program
//#####################################################
void loop() {
    while (true) {
        uint8_t receivedBytes = chekForRequest();
    }
}

//#####################################################
//# - DEBUG
//#####################################################
void printMsg(byte *data, byte len) {

    Serial.print("      STX           :");  printHex(data[0],                   "\r\n");
    Serial.print("      MSG_NO        :");  printHex(&data[MSG_NO_L], 2,        "\r\n");
    Serial.print("      from --> to   :");  Serial.print(deviceName[data[SRC_ADDR]]);Serial.print(" --> ");Serial.println(deviceName[data[DST_ADDR]]);
    Serial.print("      Messaggio     :");  printHex(&data[MSG_START], len-6,   "\r\n");
    Serial.print("      ETX           :");  printHex(data[len-1],               "\r\n");
}


//#####################################################
//# chekForRequest
//#####################################################
uint8_t chekForRequest() {
    uint8_t receivedBytes = 0;

        // Non-blocking
    receivedBytes = vw_get_messageLN(RxMsg, RX_BUFFERSIZE);

    if (receivedBytes) {
        digitalWrite(LED, true); // Flash a light to show received good message

            // -----------------------------------------------------
            // - Message with a good checksum received, dump it.
            // -----------------------------------------------------
        // Serial.print("\r\nGOT: "); printHex(RxMsg, RX_BUFFERSIZE, "\r\n");


            // Rispondi solo se il messaggio è indirizzato a questo device
            // oppure:
            //    - è un Broadcast che prevede risposta 0xFF
            //    - è un Broadcast che NON prevede risposta 0xFE ma ho dati da inviare
        if (fDEBUG) {
            Serial.print("\r\nDEBUG-GOT: "); printHex(RxMsg, receivedBytes, "\r\n");
        }

        else {
            if (RxMsg[DST_ADDR] == BROADCAST || RxMsg[DST_ADDR] == thisDevADDR )
                Serial.println("\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n");
                Serial.println("\r\nRCVED:"); printMsg(RxMsg, receivedBytes);
        }

        // delay(2000*thisDevADDR);       // porima di rispondere aspetta un tempo che dipenda dal DevAddress
        sendResponse(1000, &RxMsg[MSG_START], receivedBytes);



        if (RxMsg[DST_ADDR] == 0xFE ) {
            // if (dataToSend) sendData();
        }


        digitalWrite(LED, false);
    }

    return receivedBytes;
}


//#####################################################
// #  sendResponse()
// #  REQ: STX ! MasterAddress  ! slaveAddress    !  readPin    ! numeroPIN
// #  RSP: STX ! slaveAddress   ! masterAddress   !  readPin    ! numeroPIN, value
// #
//#####################################################
void sendResponse(int DELAY, byte *msg, byte len) {

    delay(DELAY*thisDevADDR);       // porima di rispondere aspetta un tempo che dipenda dal DevAddress
        // ---------------------------------------
        // - preparazione dati di ritorno
        // ---------------------------------------
    byte dataLen = 0;
    TxMsg[dataLen++] = STX;
    TxMsg[dataLen++] = RxMsg[MSG_NO_L];
    TxMsg[dataLen++] = RxMsg[MSG_NO_H];
    TxMsg[dataLen++] = MASTER_ADDRESS;             // Destination ADDRESS
    TxMsg[dataLen++] = thisDevADDR;               // Source Address

    // TxMsg [dataLen++] = READ_PIN_CMD;               // Definito in LnProtocol.h - Command Receviced and Executed
    // TxMsg [dataLen++] = pinNO;                      //

    for (int i=0; i<len-6; i++)
        TxMsg[dataLen++] = msg[i];


    byte CRC8value    = LnCRC8(&TxMsg[1], dataLen); // skip del STXed ETX
    // TxMsg[dataLen++] = CRC8value;
    TxMsg[dataLen++] = ETX;

        // Turn on the LED on pin LED to indicate that we are about to transmit data
    digitalWrite(LED, HIGH);

        // vw_send((byte *)TxMsg, &dataLen);
    vw_send(TxMsg, dataLen);

        // Wait until the data has been sent
    vw_wait_tx();

        // Turn off the LED on pin LED to indicate that we have now sent the data
    digitalWrite(LED, LOW);

    // --------------------------
    // - DEBUG - PRINT MESSAGE
    // --------------------------
    Serial.println("\n\rSENT :"); printMsg(TxMsg, dataLen);


}
