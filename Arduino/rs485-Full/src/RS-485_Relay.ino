/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-25_10.00.54

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428



*/


//@TODO: bisogna verificarlo
// ################################################################
// # - M A I N     Loop_Relay
// #    - riceviamo i dati da RaspBerry
// #    - facciamo il forward verso rs485
// #    - torniamo indietro la risposta
// ################################################################
void loop_Relay() {
    pData->displayData = false;                // data display dei byte hex inviati e ricevuti
    pData->timeout     = 5000;
    pData->rx[DATALEN] = 0;

    // ricezione messaggio da RaspBerry
    byte rCode = recvMsg232(pData);

    if (rCode == LN_OK) {
        fwdToRs485(pData);
        waitRs485Response(pData);
        sendMsg232(pData);
    }
}


// ################################################################
// #- riceviamo i dati da rs485
// #-  Se OK allora li torniamo al RaspBerry
// #-  Se ERROR/TIMEOUT ritorniamo errore al RaspBerry
// ################################################################
void waitRs485Response(RXTX_DATA *pData) {
    pData->timeout  = 10000;
    byte rCode      = recvMsg485(pData);

    copyRxMessageToTx(pData);

    if (rCode == LN_OK) {
        return;
    }

    else if (pData->rx[DATALEN] == 0) {
        pData->tx[CMD_RCODE] = TIMEOUT_ERROR;
        byte errorMsg[] = "Nessuna richiesta ricevuta in un tempo di 10 sec.";
        prepareMessage(pData, errorMsg, sizeof(errorMsg));
    }
}



// ################################################################
// # - Forward del messaggio ricevuto da RaspBerry verso RS485
// ################################################################
void fwdToRs485(RXTX_DATA *pData) {

    copyRxMessageToTx(pData);

        // send to RS-485 bus
    digitalWrite(RS485_ENABLE_PIN, ENA_485_TX);               // enable Rs485 sending
    sendMsg485(pData);
    digitalWrite(RS485_ENABLE_PIN, ENA_485_RX);               // set in receive mode
}



// ################################################################
// # - Forward del messaggio ricevuto da RS485 verso RaspBerry
// ################################################################
void fwdToRaspBerry(RXTX_DATA *pData) {
    copyRxMessageToTx(pData);
    sendMsg232(pData);

}
