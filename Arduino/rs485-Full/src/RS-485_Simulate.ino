/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-20_10.21.30

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
    Serial232.print(myID);Serial232.println(F("Sono in simulation mode"));
    simulateEcho(pData);
    Serial232.println();
    delay(6000);
}

// #############################################################
// # Prepariamo un pacchetto di sumulazione
// #    come se fosse rivecuto da Master (addr=0)
// #    e facciamo il forwarding sulla rs485
// #############################################################
// int seqNO = 0;
void simulateEcho(RXTX_DATA *pData) {
    static int seqNO = 0;
    pData->displayData          = true;

    pData->rx[SENDER_ADDR]      = myEEpromAddress; // SA
    pData->rx[DESTINATION_ADDR] = myEEpromAddress;  // DA
    pData->rx[SEQNO_HIGH]       = seqNO >> 8;
    pData->rx[SEQNO_LOW]        = seqNO & 0x00FF;
    pData->rx[COMMAND]          = ECHO_CMD;
    pData->rx[RCODE]            = OK;
    pData->rx[DATALEN]          = 6;

    byte data[]  = "simulated echo";
    prepareMessage(pData, data, sizeof(data));

        // send to RS-485 bus
    sendMsg485(pData);

    seqNO++;

}
#endif