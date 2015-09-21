#include <Arduino.h>
#include <VirtualWire.h>                // RX-Default D11  TX-Default D12 TX_Enable_pin D10
#include <LnFunctions.h>                // D2X(dest, val, 2), printHex()
void setup();
void loop();
void RXprocess();
void readDigitalPin(byte slaveAddress, byte pinNO);
#line 1 "src/LnProtocolMaster.ino"
/* FILE:    MXFS03V_433MHZ_MODULE_HCMODU0007_TRANSMIT_EXAMPLE.pde
   DATE:    03/03/13
   VERSION: 0.1
   AUTHOR:  Andrew Davies

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


// BOF preprocessor bug prevent - insert me on top of your arduino-code
// From: http://www.a-control.de/arduino-fehler/?lang=en
#if 1
__asm volatile ("nop");
#endif

//Include the VirtualWire library
#define DR3100x                         // altro tipo di trasmitter
//#include <VirtualWire.h>                // RX-Default D11  TX-Default D12 TX_Enable_pin D10

#define _I_AM_ARDUINO_NANO_
//#include <LnFunctions.h>                // D2X(dest, val, 2), printHex()

#define     MAX_BufferSize 200

void readDigitalPin(byte a, byte b);

    // --- Digital IO pin that will be used for sending data to the transmitter
const int   RX_433MHz_Pin    = D02;   // D2
const int   TX_433MHz_Pin    = D04;   // D4
const int   LED              = D13;  // D13


uint8_t     RECEIVED_FLAG     = 0;
bool        I_AM_MASTER       = true;
byte        counter           = 0;   // contatore per messaggi inviati



void setup() {
    Serial.begin(9600);   // Debugging only
    Serial.println("setup");

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

    // vw_setup(10000);                // Bits per sec
    vw_setup(2000);                // Bits per sec
    vw_rx_start();                      // Start the receiver PLL running

    pinMode(LED, OUTPUT);
    if (I_AM_MASTER)
        Serial.print("I am 433MHz MASTER\r\n");
    else
        Serial.print("I am 433MHz SLAVE\r\n");
}

//#####################################################
//# - Main program
//#####################################################
void loop() {
    if (I_AM_MASTER) {
        // TXprocess();
        readDigitalPin(2, 5);
        delay(1000);
        RXprocess();
        delay(3000);
    }

    else {
        RXprocess();
        if (RECEIVED_FLAG == true) {
            delay(1000);
            // TXprocess();
        }
    }
}


//#####################################################
//# RXprocess
//#####################################################
void RXprocess() {
    byte RxMsg[MAX_BufferSize];
    byte RxBufferSize=MAX_BufferSize;


        // Non-blocking
    uint8_t RECEIVED_FLAG = vw_get_message(RxMsg, &RxBufferSize);
    if (RECEIVED_FLAG) {
        byte i;

        digitalWrite(LED, true); // Flash a light to show received good message

        // -----------------------------------------------------
        // - Message with a good checksum received, dump it.
        // -----------------------------------------------------
        Serial.print("GOT: "); printHex(RxMsg, RxBufferSize, "\r\n");

        digitalWrite(LED, false);
    }
}


//#####################################################
// #  readDigitalPin()
// #  REQ: STX ! MasterAddress  ! slaveAddress    !  readPin    ! numeroPIN
// #  RSP: STX ! slaveAddress   ! masterAddress   !  readPin    ! numeroPIN, value
// #
//#####################################################
void readDigitalPin(byte slaveAddress, byte pinNO) {
    byte TxMsg[MAX_BufferSize];
    byte i;

    byte dataLen = 0;
    TxMsg [dataLen++] = ++counter;   // DEBUG - Andrà tolto nella versione definitiva.
    TxMsg [dataLen++] = STX;
    TxMsg [dataLen++] = MASTER_ADDRESS;
    TxMsg [dataLen++] = slaveAddress;
    TxMsg [dataLen++] = READ_PIN_CMD;
    TxMsg [dataLen++] = pinNO;
    byte CRC8value    = LnCRC8(&TxMsg[1], dataLen); // skip del STXed ETX
    TxMsg [dataLen++] = CRC8value;
    TxMsg [dataLen++]   = ETX;

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
    Serial.print("SENT: "); printHex(TxMsg, dataLen, "\r\n");

}
