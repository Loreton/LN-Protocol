/*
Author:     Loreto Notarantonio
version:    LnVer_2017-08-09_17.13.36

Scope:      Funzioni comuni

*/
#if 0

// ################################################################
// # - setMyID
// # char myID[] = "\r\n[Slave-xxx] - "; // i primi due byte sono CR e LF
// ################################################################
void setMyID(const char *name) {
    byte i=3;
    byte i1;

    for (i1=0; i1<5; i1++) {
        myID[i++] = name[i1];
    }
    i++; // skip '-'

    unsigned char *xx = LnUtoa(myEEpromAddress, 3, '0');
    myID[i++] = xx[0];
    myID[i++] = xx[1];
    myID[i++] = xx[2];

    if (pData->fDisplayMyData) pData->myID = myID;
}
#endif

void setMyID(const char *name) {
    // char myID[] = "\r\n[YYYYY-xxx] - "; // i primi due byte saranno CR e LF
                                        // YYYYY Emula, Relay, Slave
    myID = LnJoinStr("\r\n[", name, "-", LnUtoa(myEEpromAddress, 3, '0'), "] - ", NULL);

    pData->myID = myID;
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
// # Inserisce un messaggio (di errore o altro) nella parte CommandData
// #############################################################
void setTxCommandData(RXTX_DATA *pData, char cmdData[], byte dataLen=0) {
    if (dataLen==0) {
        const char *ptr = cmdData;
        while (*ptr++) {dataLen++; }
    }

    byte index = COMMAND_DATA-1;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData->tx[++index] = cmdData[i];         // copiamo i dati nel buffer da inviare

    pData->tx[DATALEN] = --index;  // update dataLen
    // displayMyData(INO_Prefix,  LN_OK, pData);
}


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

        setTxCommandData(pData, errorMsg, sizeof(errorMsg));
    }


    return rcvdRCode;
}



