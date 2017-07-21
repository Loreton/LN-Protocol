/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-21_10.05.51

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


// const char INO_RX[] = "RX-ino";
// const char INO_TX[] = "TX-ino";
// #############################################################
// # Inserisce nella risposta un messaggio (di errore o altro)
// #############################################################
void prepareMessage(RXTX_DATA *pData, byte data[], byte dataLen) {
    // displayMyData(INO_RX,  LN_OK, pData, false);
    copyRxMessageToTx(pData); // ci portiamo anche il numero messaggio...
    // displayMyData(INO_TX,  LN_OK, pData, false);


    byte index = USER_DATA-1;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData->tx[++index] = data[i];         // copiamo i dati nel buffer da inviare


    pData->tx[DATALEN] = --index;  // update dataLen
    // displayMyData(INO_TX,  LN_OK, pData, false);
}


// ################################################################
// # --- DISPLAY DATA
// ################################################################
// void rxDisplayData(byte rCode, RXTX_DATA *pData) {
//     displayDebugMessage("RX-inoData", rCode, pData->rx);
//     displayDebugMessage("RX-inoRaw ", rCode, pData->raw);
// }
// void txDisplayData(byte rCode, RXTX_DATA *pData) {
//     displayDebugMessage("TX-inoRaw ", rCode, pData->raw);
//     displayDebugMessage("TX-inoData", rCode, pData->tx);
// }



