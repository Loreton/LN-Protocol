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
#include "LnProtocolMonitor.h"




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
//# - Main program
//#####################################################
void loop() {

    while (true) {
        chekForRequest();
        delay(10);
    }
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

