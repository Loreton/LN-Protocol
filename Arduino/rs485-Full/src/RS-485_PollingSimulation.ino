/*
Author:     Loreto Notarantonio
version:    LnVer_2017-08-13_10.05.37

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/


#ifdef POLLING_SIMULATION
// byte returnRS485 = true; // simuliamo anche il ritorno in 485 sulla seriale per affinare il master python
byte returnRS485 = false; // simuliamo anche il ritorno in 485 sulla seriale per affinare il master python
// ##########################################################
// se vogliamo che Arduino invii un echo autonomamente
// ##########################################################
void loop_PollingSimulation() {
    if (firstRun) {
        setMyID("Emula");
    }

    if (returnRS485) {
        pData->fDisplayMyData    = false;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherData = false;               // display dati relativi ad  altri indirizzi
        pData->fDisplayRawData   = false;                // display raw data
        PollingSimulation(pData);
    }
    else {
        pData->fDisplayMyData    = true;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherData = false;               // display dati relativi ad  altri indirizzi
        pData->fDisplayRawData   = false;                // display raw data
        Serial.print(myID);Serial.println(F("Sono in Polling simulation mode"));
        // Serial.println(joinStr(myID, "Sono in Polling simulation mode", NULL));

        PollingSimulation(pData);
        Serial.println();
    }


    delay(10000);
}

// #############################################################
// # Prepariamo un pacchetto di sumulazione
// #    come se fosse invocato da Master (addr=0)
// #    ...facciamo il forwarding sulla rs485
// #    ...attendiamo la risposta
// #    ...inviamo il pacchetto verso Master.
// #############################################################
void PollingSimulation(RXTX_DATA *pData) {
    static int seqNO   = 0;
    volatile byte i;

    int destAddresses[] = {11, 12, 13};
    // int destAddresses[] = {11};
    byte nElem = sizeof(destAddresses)/sizeof(int);



    for (i=0; i<nElem; i++) {
            // ---------------------------------------------------------
            // - dovendo simulare la ricezione da parte del raspberry
            // - preparo un messaggio come se fosse stato ricevuto
            // ---------------------------------------------------------
        pData->rx[SENDER_ADDR]      = myEEpromAddress; // SA
        pData->rx[DESTINATION_ADDR] = destAddresses[i];                    // DA
        pData->rx[SEQNO_HIGH]       = seqNO >> 8;
        pData->rx[SEQNO_LOW]        = seqNO & 0x00FF;
        pData->rx[CMD_RCODE]        = OK;
        pData->rx[COMMAND]          = POLLING_CMD;
        pData->rx[SUBCOMMAND]       = REPLY;
        pData->rx[DATALEN]          = SUBCOMMAND;


            // come comandData inviamo un testo di esempio
        char data[]  = "Polling request!";
        setCommandData(pData->rx, data);
        // setTxCommandData(pData, data);

            // lo copiammo nel TX
        copyRxMessageToTx(pData);
            // send it to RS-485 bus
        sendMsg485(pData);

            // wait for response
        byte rcvdRCode = waitRs485Response(pData, 2000);
        if (rcvdRCode == LN_OK) {
            copyRxMessageToTx(pData);
        }
        else { // il messaggio dovrebbe ancora essere nel TX
            // int dataLen = joinString(LnFuncWorkingBuff, "[", errMsg[rcvdRCode], "]",  "occurred on Polling request!");
            // setTxCommandData(pData, LnFuncWorkingBuff, dataLen);
            char *pippo = joinStr("[", errMsg[rcvdRCode],"] occurred on Polling request!", NULL);
            setCommandData(pData->tx, pippo);
            // setTxCommandData(pData, pippo);
            pData->tx[CMD_RCODE] = rcvdRCode;
        }

            // inviamo sulla 232 in formato rs485
        if (returnRS485) {
            sendMsg232(pData);
        }
            // ... oppure lo inviamo sulla 232 in formato ascii
        else {
            Serial.print(F("\n\n"));
            displayMyData("TX-poll", rcvdRCode, pData);
        }

        delay(10000); // aspettiamo 10 secondi tra un indirizzo ed il successivo
    }
    seqNO++;

}
#endif