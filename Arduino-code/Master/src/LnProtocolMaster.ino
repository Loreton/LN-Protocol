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


#define _I_AM_MAIN_
#include "LnProtocolMaster.h"




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

    vw_setup(BITS_PER_SEC);
    vw_rx_start();                      // Start the receiver PLL running

    pinMode(LED, OUTPUT);



}
//#####################################################
//# - ifMaster()
//#####################################################
bool ifMaster(void) {
bool I_AM_MASTER    = true;
bool prevFLAG       = ! I_AM_MASTER;

    // Serial.println(I_AM_MASTER);
        // eventuale change del ruolo
    if (I_AM_MASTER != prevFLAG) {
        prevFLAG = I_AM_MASTER;

        if (I_AM_MASTER) {
            Serial.print("I am 433MHz MASTER\r\n");
        }
        else {
            Serial.print("I am 433MHz SLAVE\r\n");
        }
    }

    // Serial.println(I_AM_MASTER);
    return I_AM_MASTER;
}

//#####################################################
//# - Main program
//#####################################################
void loop() {
    if (ifMaster())
        loopMASTER();
    else
        loopSLAVE();
}

//#####################################################
//# - loopSLAVE
//#####################################################
void loopSLAVE() {

    while (true) {
        chekForRequest();
        delay(10);
    }
}

//#####################################################
//# - loopMASTER
//#####################################################
void loopMASTER() {
    byte slaveAddr = 2;
    byte pinNO = 5;
    // uint8_t RECEIVED_FLAG;


    readDigitalPin(slaveAddr, pinNO);
    delay(1000); // wait for turn-around
    Serial.println("      waiting for response: ");
    uint8_t RECEIVED_FLAG = getResponse(5000);
    if (RECEIVED_FLAG == true) {
        Serial.println("Processamento della risposta");
    }
    delay(1000);

}


//#####################################################
//# chekForRequest
//#####################################################
uint8_t chekForRequest() {
    byte RxMsg[MAX_BufferSize];
    byte RxBufferSize=MAX_BufferSize;
    uint8_t RECEIVED_FLAG = 0;

        // Non-blocking
    RECEIVED_FLAG = vw_get_message(RxMsg, &RxBufferSize);

    if (RECEIVED_FLAG) {
        digitalWrite(LED, true); // Flash a light to show received good message

        // -----------------------------------------------------
        // - Message with a good checksum received, dump it.
        // -----------------------------------------------------
        Serial.print("\r\nGOT: "); printHex(RxMsg, RxBufferSize, "\r\n");

        digitalWrite(LED, false);
    }

    return RECEIVED_FLAG;
}

//#####################################################
//# getResponse
//#####################################################
uint8_t getResponse(int mSecTIMEOUT) {
    int sleepVAL = 500;   // mSec
    byte RxMsg[MAX_BufferSize];
    byte RxBufferSize=MAX_BufferSize;
    uint8_t RECEIVED_FLAG = 0;

    while (mSecTIMEOUT > 0) {
            // Non-blocking
        RECEIVED_FLAG = vw_get_message(RxMsg, &RxBufferSize);
        if (RECEIVED_FLAG) {

            digitalWrite(LED, true); // Flash a light to show received good message

            // -----------------------------------------------------
            // - Message with a good checksum received, dump it.
            // -----------------------------------------------------
            Serial.print("GOT: "); printHex(RxMsg, RxBufferSize, "\r\n");

            digitalWrite(LED, false);
            mSecTIMEOUT = 0;
        }
        else {
            delay(sleepVAL);
            // Serial.print("              still waiting for: ");Serial.print(mSecTIMEOUT);Serial.println(" mSec");
        }
        mSecTIMEOUT -= sleepVAL;
    }
    return RECEIVED_FLAG;
}

#if 0
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
    TxMsg [dataLen++] = ETX;

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
#endif