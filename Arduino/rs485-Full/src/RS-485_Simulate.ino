/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-13_08.32.32

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/


#ifdef SIMULATE_ECHO
// ##########################################################
// se vogliamo che Arduino invii un echo autonomamente
// ##########################################################
void loop_Simulate() {
    // Serial232.println("\r\nSono in simulation mode\r\n");
    simulateEcho(pData);
    delay(1000);
}

// #############################################################
// # Prepariamo un pacchetto di sumulazione
// #    come se fosse rivecuto da Master (addr=0)
// #    e facciamo il forwarding sulla rs485
// #############################################################
// int seqNO = 0;
void simulateEcho(RXTX_DATA *pData) {
    static int seqNO = 0;

    pData->rx[SENDER_ADDR]      = 0;    // SA
    pData->rx[DESTINATION_ADDR] = myEEpromAddress;    // DA
    pData->rx[SEQNO_HIGH]       = seqNO >> 8;
    pData->rx[SEQNO_LOW]        = seqNO & 0x00FF;
    pData->rx[COMMAND]          = ECHO_CMD;


    byte data[]  = "simulated echo";
    byte dataLen = sizeof(data);
    byte index = PAYLOAD;
    for (byte i=0; i<dataLen; i++)
        pData->rx[index++] = data[i];         // copiamo i dati nel buffer da inviare

    pData->rx[DATALEN] = index;  // set dataLen

    forwardMessage(pData);

    seqNO++;

}
#endif