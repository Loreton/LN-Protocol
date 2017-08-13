/*
Author:     Loreto Notarantonio
version:    LnVer_2017-08-13_18.22.24

Scope:      Funzioni comuni

*/



#if 0
// ################################################################
// # - Copia l'intero messaggio
// # -  RxBuffer --> TxBuffer
// ################################################################
void OOLLDD_copyRxMessageToTx(RXTX_DATA *pData) {
        // - copy ALL rx to tx
    for (byte i = 0; i<=pData->rx[DATALEN]; i++)
        pData->tx[i] = pData->rx[i];         // copiamo i dati nel buffer da inviare
}

// #############################################################
// # Inserisce un messaggio (di errore o altro) nella parte CommandData
// #############################################################
void setCommandData(byte *pData, char cmdData[], byte dataLen=0) {
    if (dataLen==0) {
        dataLen = stringLen(cmdData);
    }


    byte index = COMMAND_DATA-1;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData[++index] = cmdData[i];         // copiamo i dati nel buffer da inviare

    pData[DATALEN] = --index;  // update dataLen
    // displayMyData(INO_Prefix,  LN_OK, pData);
}

#endif

// ################################################################
// #- riceviamo i dati da rs485
// #-  Se OK allora li torniamo al RaspBerry
// #-  Se ERROR/TIMEOUT ritorniamo errore al RaspBerry
// --------------------------------------
// - se corretto:
// -    1. copia Rx to Tx
// -    2. ritorna rCode
// -    3. copia comunque su Txdata
// -    4. Se ricezione OK:
// -        4a. copia messaggio su TX
// -        4a. ruota pacchetto verso PI
// -    5. Se ricezione NOT OK:
// - altrimenti:
// -    1. copia Rx to Tx
// -    2. prepara messaggo di errore
// - finally:
// -    1. ritorna rCode
// --------------------------------------
// ################################################################
byte waitRs485Response(RXTX_DATA *pData, unsigned long TIMEOUT) {
//@todo: completare la parte di heard
        // - copy Header in caso di Timeout o altro
    byte savedHeader[SUBCOMMAND];
    for (byte i=0; i<SUBCOMMAND; i++)
        savedHeader[i] = pData->tx[i];         // copiamo i dati nel buffer da inviare


    pData->timeout = TIMEOUT;

    byte rcvdRCode = recvMsg485(pData);

    if (rcvdRCode == LN_OK) {
        copyRxMessageToTx(pData);
    }
    else {
        for (byte i=0; i<SUBCOMMAND; i++)
            pData->tx[i] = savedHeader[i];         // copiamo i dati nel buffer da inviare
        copyRxMessageToTx(pData);
                             //-- 01234567
        char errorMsg[] = "ERROR [........] occurred...!";
        const char *ptr = errMsg[rcvdRCode];

        for (byte i=7; *ptr != '\0'; i++, ptr++)
            errorMsg[i] = *ptr;

        setCommandData(pData->tx, errorMsg, sizeof(errorMsg));
        // setTxCommandData(pData, errorMsg, sizeof(errorMsg));
    }


    return rcvdRCode;
}



