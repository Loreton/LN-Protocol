/*
Author:     Loreto Notarantonio
version:    LnVer_2017-11-30_19.07.33

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.


*/



// ################################################################
// # - M A I N     Loop_Relay
// #    - riceviamo i dati da RaspBerry
// #    - facciamo il forward verso rs485
// #    - torniamo indietro la risposta
// ################################################################
void Relay_Main() {
unsigned char *Rx = pData->rx;
unsigned char *Tx = pData->tx;

    if (firstRun) {     // Il relay on deve scrivere sulla seriale in chiaro
        pData->fDisplayMyData       = false;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherHeader  = false;                // display dati relativi ad  altri indirizzi
        pData->fDisplayOtherFull    = false;                // display dati relativi ad  altri indirizzi
        pData->fDisplayRawData      = false;                // display raw data
    }

    pData->timeout         = RECV_DEFAULT_TIMEOUT; // re-set timeout to default value
    pData->rx[fld_DATALEN] = 0;

        // --------------------------------------
        // - ricezione messaggio da RaspBerry
        // --------------------------------------
    byte rCode = recvMsg232(pData);
    Rx = pData->rx;
    Tx = pData->tx;
    byte senderAddr = Rx[fld_SENDER_ADDR];
    byte destAddr   = Rx[fld_DESTINATION_ADDR];

    // delay(1000)


        // --------------------------------------
        // - se corretto:
        // -    1. inoltra to rs485 bus
        // -    2. attendi risposta
        // -    3. copia comunque su Txdata
        // -    4. Se ricezione OK:
        // -        4a. copia messaggio su TX
        // -        4a. ruota pacchetto verso PI
        // -    5. Se ricezione NOT OK:
        // -        5a. prepara messaggo di errore
        // -        5b. ruota pacchetto verso PI
        // - altrimenti:
        // -    1. ignora
        // --------------------------------------
    if (rCode == LN_OK) {
        if (destAddr == myEEpromAddress)  {
            copyRxMessageToTx(pData);
            Tx[fld_DESTINATION_ADDR] = Rx[fld_SENDER_ADDR];
            Tx[fld_SENDER_ADDR]      = myEEpromAddress;
            char respMSG[] = "Echo Relay response!";
            setDataCommand(Tx, respMSG, sizeof(respMSG));
            Tx[fld_CMD_RCODE] = OK;
            sendMsg232(pData);


        }
        else {
            Relay_fwdToRs485(pData);
                // qualsiasi esito il msg è pronto da inviare sulla rs232
            byte rcvdRCode = Relay_waitRs485Response(pData, 2000);
            Relay_fwdToRaspBerry(pData, rcvdRCode);
        }
    }


}


// ################################################################
// # - Forward del messaggio ricevuto da RaspBerry verso RS485
// ################################################################
void Relay_fwdToRs485(RXTX_DATA *pData) {

    copyRxMessageToTx(pData);
        // send to RS-485 bus
    sendMsg485(pData);

}



// ################################################################
// # - Forward del messaggio ricevuto da RS485 verso RaspBerry
// ################################################################
void Relay_fwdToRaspBerry(RXTX_DATA *pData, byte rcvdRCode) {
    copyRxMessageToTx(pData);

    #ifdef RETURN_TEXT_DATA_TO_MASTER
        // inviamo sulla 232 in formato ascii
        displayMyData("RX-poll", rcvdRCode, pData);
    #else
        // ... oppure lo inviamo in formato rs485
        sendMsg232(pData);
    #endif

}



// ################################################################
// #- riceviamo i dati da rs485
// #-  Se OK allora li torniamo al RaspBerry
// #-  Se ERROR/TIMEOUT ritorniamo errore al RaspBerry
// --------------------------------------
// - se corretto:
// -    1. nothing
// - altrimenti:
// -    1. prepara messaggo di errore
// -    2. set opportunamente gli indirizzi
// - finally:
// -    2. ritorna rCode
// --------------------------------------
// ################################################################
byte Relay_waitRs485Response(RXTX_DATA *pData, unsigned long TIMEOUT) {

    pData->timeout = TIMEOUT;

    byte rcvdRCode = recvMsg485(pData);


        // --------------------------------------------------------
        // - vuol dire che lo slave non ha risposto
        // - o comunque ci sono stati errori nella trasmissione
        // --------------------------------------------------------
    if (rcvdRCode != LN_OK) {

        // -----------------------------------------
        // - Prepariamo il messaggio di errore
        // - lo scriviamo su ->rx
        // - perché poi sarà copiato su ->tx
        // -----------------------------------------
        pData->rx[fld_SENDER_ADDR]      = pData->rx[fld_DESTINATION_ADDR];
        pData->rx[fld_DESTINATION_ADDR] = 0;

                      //-- 01234567
        char errorMsg[] = "ERROR: ........ occurred!";
        const char *ptr = errMsg[rcvdRCode];

        // copiamo il codice errore nei [....]
        for (byte i=7; *ptr != '\0'; i++, ptr++)
            errorMsg[i] = *ptr;

        setDataCommand(pData->rx, errorMsg, sizeof(errorMsg));

    }
    return rcvdRCode;
}