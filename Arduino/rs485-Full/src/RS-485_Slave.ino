/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-25_11.40.12

Scope:      Funzione di slave.
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/


// ################################################################
// # - M A I N     Loopslave
// #    - riceviamo i dati da rs485
// #    - elaboriamo il comando ricevuto
// #    - rispondiamo se siamo interessati
// ################################################################
void loop_Slave() {
    pData->displayData      = true;                // data display dei byte
    pData->displayRawData   = false;              // display dei raw data
    pData->timeout          = 20000;

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
        Serial.print(F(" - Nessuna richiesta ricevuta in un tempo di mS: "));
        Serial.print(pData->timeout);
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
// const char INO_RX[] = "RX-slave";
void processRequest(RXTX_DATA *pData) {
        // - DEBUG - display comments to serial
    byte senderAddr = pData->rx[SENDER_ADDR];
    byte destAddr   = pData->rx[DESTINATION_ADDR];
    // byte comando    = pData->rx[COMMAND];
    // int seqNO       = pData->rx[SEQNO_HIGH]*256 + pData->rx[SEQNO_LOW];

    // Serial.print(myID);Serial.print(INO_RX);Serial.println();
    // Serial.print(TAB);Serial.print(F("from : ")); Serial.print(senderAddr);Serial.println();
    // Serial.print(TAB);Serial.print(F("to   : ")); Serial.print(destAddr);Serial.println();
    // Serial.print(TAB);Serial.print(F("CMD  : ")); Serial.print(comando);Serial.println();
    // Serial.print(TAB);Serial.print(F("seqNo: ")); Serial.print(LnUtoa(seqNO,5,'0'));Serial.println();


    if (destAddr != myEEpromAddress) {    // non sono io.... commento sulla seriale
        Serial.println("\n\n");
        Serial.print(TAB);Serial.print(F("Request is NOT for me\n\n\n"));
        // displayMyData(INO_RX,  LN_OK, pData, false);
        return;
    }


    byte myMsg1[] = "devo leggere il pin";
    byte myMsg2[] = "devo scrivere il pin";
    byte myMsg3[] = "Comando non riconosciuto";

    // sono io.... process request
    Serial.println("\n\n");
    Serial.print(TAB);Serial.print(F("   (Request is for me) ... answering\n\n\n"));
    switch (pData->rx[COMMAND]) {

        case POLLING_CMD:
            if (pData->rx[SUBCOMMAND] == REPLY) {
                pData->tx[CMD_RCODE] = OK;
                prepareMessage(pData, myMsg1, sizeof(myMsg1));
            }
            break;

        case READPIN_CMD:
            pData->tx[CMD_RCODE] = OK;
            prepareMessage(pData, myMsg1, sizeof(myMsg1));
            break;

        case WRITEPIN_CMD:
            pData->tx[CMD_RCODE] = OK;
            prepareMessage(pData, myMsg2, sizeof(myMsg2));
            break;

        default:
            pData->tx[CMD_RCODE] = UNKNOWN_CMD;
            prepareMessage(pData, myMsg3, sizeof(myMsg3));
            break;
    }

    pData->tx[DESTINATION_ADDR] = senderAddr;
    pData->tx[SENDER_ADDR]      = myEEpromAddress;
    sendMsg485(pData);
}
