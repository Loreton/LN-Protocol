/*
Author:     Loreto Notarantonio
version:    LnVer_2017-08-13_10.33.54

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
void rs485_Relay() {
    if (firstRun) {
        // pData->fDisplayData    = true;                // display user/command data

        pData->fDisplayMyData    = true;                // display dati relativi al mio indirizzo
        pData->fDisplayOtherData = true;                // display dati relativi ad  altri indirizzi
        pData->fDisplayRawData = false;                // display raw data
        // pData->fDisplayAllPckt = true;                // display all source/destination packets

        setMyID("Relay");
    }

    pData->timeout     = 5000;
    pData->rx[DATALEN] = 0;

        // --------------------------------------
        // - ricezione messaggio da RaspBerry
        // --------------------------------------
    byte rCode = recvMsg232(pData);
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
        fwdToRs485(pData);
            // qualsiasi esito il msg è pronto da inviare sulla rs232
        waitRs485Response(pData, 2000);
        sendMsg232(pData);
    }
}


// ################################################################
// # - Forward del messaggio ricevuto da RaspBerry verso RS485
// ################################################################
void fwdToRs485(RXTX_DATA *pData) {

    copyRxMessageToTx(pData);
        // send to RS-485 bus
    sendMsg485(pData);

}



// ################################################################
// # - Forward del messaggio ricevuto da RS485 verso RaspBerry
// ################################################################
void fwdToRaspBerry(RXTX_DATA *pData) {
    copyRxMessageToTx(pData);
    sendMsg232(pData);

}
