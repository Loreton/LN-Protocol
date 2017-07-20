/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-20_09.35.27

Scope:      Funzioni comuni

*/


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
// # Inserisce nella risposta un messaggio (di errore o altro)
// #############################################################
void prepareMessage(RXTX_DATA *pData, byte data[], byte dataLen) {
    copyRxMessageToTx(pData); // ci portiamo anche il numero messaggio...
    byte index = USER_DATA;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData->tx[index++] = data[i];         // copiamo i dati nel buffer da inviare


    pData->tx[DATALEN] = index;  // update dataLen
}


// ################################################################
// # --- DISPLAY DATA
// ################################################################
void rxDisplayData(byte rCode, RXTX_DATA *pData) {
    displayDebugMessage("inoRECV-raw ", rCode, pData->raw);
    displayDebugMessage("inoRECV-data", rCode, pData->rx);
}
void txDisplayData(byte rCode, RXTX_DATA *pData) {
    displayDebugMessage("inoSEND-raw ", rCode, pData->raw);
    displayDebugMessage("inoSEND-data", rCode, pData->tx);
}



