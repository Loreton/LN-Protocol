/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-26_17.31.24

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/


#ifdef POLLING_SIMULATION
// ##########################################################
// se vogliamo che Arduino invii un echo autonomamente
// ##########################################################
void loop_PollingSimulation() {
    pData->fDisplayData    = true;                // display user/command data
    pData->fDisplayRawData = false;                // display raw data
    pData->fDisplayAllPckt = false;                // display all source/destination packets

    Serial232.print(myID);Serial232.println(F("Sono in Polling simulation mode"));
    PollingSimulation(pData);
    Serial232.println();
    delay(10000);
}

// #############################################################
// # Prepariamo un pacchetto di sumulazione
// #    come se fosse rivecuto da Master (addr=0)
// #    e facciamo il forwarding sulla rs485
// #############################################################
void PollingSimulation(RXTX_DATA *pData) {
    static int seqNO   = 0;
    volatile byte i;


    int destAddresses[] = {11, 12, 13};
    // int destAddresses[] = {11};
    byte nElem = sizeof(destAddresses)/sizeof(int);

    for (i=0; i<nElem; i++) {
        pData->rx[SENDER_ADDR]      = myEEpromAddress; // SA
        pData->rx[DESTINATION_ADDR] = destAddresses[i];                    // DA
        pData->rx[SEQNO_HIGH]       = seqNO >> 8;
        pData->rx[SEQNO_LOW]        = seqNO & 0x00FF;
        pData->rx[CMD_RCODE]        = OK;
        pData->rx[COMMAND]          = POLLING_CMD;
        pData->rx[SUBCOMMAND]       = REPLY;
        pData->rx[DATALEN]          = SUBCOMMAND;
        // Serial.print("SUBCOMMAND... "); Serial.println(pData->rx[SUBCOMMAND]);

        byte data[]  = "polling simulation.";
        prepareMessage(pData, data, sizeof(data));

            // send to RS-485 bus
        sendMsg485(pData);
            // wait for response
        byte rcvdRCode = waitRs485Response(pData);
            // ne facciamo il solo display
        displayMyData("TX-poll", rcvdRCode, pData);
        delay(2000);
    }
    Serial.print("\n\n\n");
    seqNO++;

}
#endif