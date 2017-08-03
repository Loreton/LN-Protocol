/*
Author:     Loreto Notarantonio
version:    LnVer_2017-08-03_08.04.58

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
// ################################################################
void loop_Slave() {
    if (firstRun) {
        setMyID("Slave");
        pData->fDisplayData    = true;                // display user/command data
        pData->fDisplayRawData = false;                // display raw data
        pData->fDisplayAllPckt = false;                // display all source/destination packets
        pData->timeout         = 20000;
    }

    Serial.println();
    // Serial.print(myID);printNchar('-', 60);
    byte rCode = recvMsg485(pData);

    if (rCode == LN_OK) {
        processRequest(pData);
        Serial.println();
    }

        // lo slave scrive sulla seriale come debug
    else if (pData->rx[DATALEN] == 0) {
        Serial.print(myID);
        Serial.print(F("rCode: "));Serial.print(rCode);
        Serial.print(F(" - Nessuna richiesta ricevuta in un tempo di mS: "));Serial.print(pData->timeout);
        Serial.println();
    }

    else { // DEBUG
        // rxDisplayData(rCode, pData);
        Serial.println();
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

    byte myMsg1[] = "Polling answer!";
    byte myMsg2[] = "devo scrivere il pin";
    byte myMsg3[] = "Comando non riconosciuto";

    switch (pData->rx[COMMAND]) {

        case POLLING_CMD:
            if (pData->rx[SUBCOMMAND] == REPLY) {
                Serial.print("\n\n");Serial.print(TAB);Serial.println(F("preparing response message... "));
                prepareMessage(pData, myMsg1, sizeof(myMsg1));
                pData->tx[CMD_RCODE] = OK;
            }
            break;

        case READPIN_CMD:
            prepareMessage(pData, myMsg1, sizeof(myMsg1));
            pData->tx[CMD_RCODE] = OK;
            break;

        case WRITEPIN_CMD:
            prepareMessage(pData, myMsg2, sizeof(myMsg2));
            pData->tx[CMD_RCODE] = OK;
            break;

        default:
            prepareMessage(pData, myMsg3, sizeof(myMsg3));
            pData->tx[CMD_RCODE] = UNKNOWN_CMD;
            break;
    }

    pData->tx[DESTINATION_ADDR] = senderAddr;
    pData->tx[SENDER_ADDR]      = myEEpromAddress;
    sendMsg485(pData);
}
