/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-19_18.34.35

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
    byte rCode         = recvMsg232(pData);

    if (rCode == LN_OK) {
        fwdToRs485(pData);
            // -------- E C H O  ----------
            // invia il messaggio anche indietro a raspBerry
        if (pData->rx[COMMAND] == CMD_ECHO) {
            fwdToRaspBerry(pData);
        }
        else {
            waitRs485Response(pData);
            sendMsg232(pData);
        }
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
        pData->tx[RCODE] = ERROR_TIMEOUT;
        byte errorMsg[] = "Nessuna richiesta ricevuta in un tempo di 10 sec.";
        prepareErrorMessage(pData, errorMsg, sizeof(errorMsg));
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


// ################################################################
// # - Copia l'intero messaggio
// # -  RxBuffer --> TxBuffer
// ################################################################
void copyRxMessageToTx(RXTX_DATA *pData) {
        // - copy ALL rx to tx
    for (byte i = 0; i<=pData->rx[DATALEN]; i++)
        pData->tx[i] = pData->rx[i];         // copiamo i dati nel buffer da inviare
}


// #############################################################
// # Inserisce nel messaggio il testo di errore
// #############################################################
void prepareErrorMessage(RXTX_DATA *pData, byte data[], byte dataLen) {
    byte index = USER_DATA;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData->tx[index++] = data[i];         // copiamo i dati nel buffer da inviare


    pData->tx[DATALEN] = index;  // update dataLen
}
