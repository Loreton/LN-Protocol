/*
Author:     Loreto Notarantonio
version:    LnVer_2017-08-09_17.35.51

Scope:      Funzione di slave.
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/

// bool firstRun = true;
// ################################################################
// # - M A I N     Loopslave
// #    - riceviamo i dati da rs485
// #    - elaboriamo il comando ricevuto
// #    - rispondiamo se siamo interessati
// lo slave scrive sulla seriale come debug
// ################################################################
void loop_Slave() {
    if (firstRun) {
        // pData->fDisplayData     = true;                // display user/command data
        pData->fDisplayMyData    = true;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherData = false;                // display dati relativi ad  altri indirizzi

        // pData->fDisplayAllPckt  = false;                // display all source/destination packets
        pData->fDisplayRawData  = false;                // display raw data
        pData->timeout          = 5000;
        setMyID("Slave");
    }

    // Serial.println();
    byte rcvdRCode = recvMsg485(pData);

    if (rcvdRCode == LN_OK) {
        processRequest(pData);
        // Serial.println();
    }

    else if (pData->rx[DATALEN] == 0) {
        Serial.print(myID);
        Serial.print(F("rcvdRCode: "));Serial.print(rcvdRCode);
        Serial.print(F(" - Nessuna richiesta ricevuta in un tempo di mS: "));Serial.print(pData->timeout);
        Serial.println();
        // Serial.println(LnJoinStr(myID, "rcvdRCode: ", LnUtoa(rcvdRCode, 3, 0), " - Nessuna richiesta ricevuta in un tempo di mS: ", LnUtoa(pData->timeout, 3, 0), NULL));
        // Serial.println(pippo);
        // free(pippo);

    }

    else { // DEBUG
        // rxDisplayData(rCode, pData);
        // Serial.println();
    }

}



// #############################################################
// #
// #############################################################
void processRequest(RXTX_DATA *pData) {
    byte senderAddr = pData->rx[SENDER_ADDR];
    byte destAddr   = pData->rx[DESTINATION_ADDR];

    if (destAddr != myEEpromAddress) {    // non sono io.... commento sulla seriale
        return;
    }
//@todo: inserire l'indirizzo nel comando myMsg...
    char myMsg1[] = "Polling answer!";
    char myMsg2[] = "devo scrivere il pin";
    char myMsg3[] = "Comando non riconosciuto";

    copyRxMessageToTx(pData);
    switch (pData->rx[COMMAND]) {

        case POLLING_CMD:
            if (pData->rx[SUBCOMMAND] == REPLY) {
                Serial.print("\n\n");Serial.print(TAB);Serial.println(F("preparing response message... "));
                // char *pippo = LnJoinStr("\n\n", TAB, "preparing response message... ", NULL);
                // Serial.println(pippo);
                // free(pippo);

                setTxCommandData(pData, myMsg1, sizeof(myMsg1));
                pData->tx[CMD_RCODE] = OK;
            }
            break;

        case READPIN_CMD:
            setTxCommandData(pData, myMsg1, sizeof(myMsg1));
            pData->tx[CMD_RCODE] = OK;
            break;

        case WRITEPIN_CMD:
            setTxCommandData(pData, myMsg2, sizeof(myMsg2));
            pData->tx[CMD_RCODE] = OK;
            break;

        default:
            setTxCommandData(pData, myMsg3, sizeof(myMsg3));
            pData->tx[CMD_RCODE] = UNKNOWN_CMD;
            break;
    }

    pData->tx[DESTINATION_ADDR] = senderAddr;
    pData->tx[SENDER_ADDR]      = myEEpromAddress;
    sendMsg485(pData);
}
