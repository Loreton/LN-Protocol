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
void Relay_Main(unsigned long RxTimeout) {
    pData->Rx_Timeout      = RxTimeout;         // set timeout
    while (true) {
        Rx[fld_DATALEN] = 0;

            // --------------------------------------
            // - ricezione messaggio da RaspBerry
            // --------------------------------------
        byte rCode = recvMsg232(pData);
        // Rx = pData->rx;
        // Tx = pData->tx;


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

        if (rCode == LN_TIMEOUT) {
            if (returnRs485ToMaster) {
                // Serial.print(myID); Serial.print(F(" sono in TIMEOUT"));Serial.println();
                /* solo per eventuale DEBUG
                copyRxMessageToTx(pData);
                char noDataRcvd[] = " - waiting for data ... ";
                setDataCommand(Tx, noDataRcvd, sizeof(noDataRcvd));
                Tx[fld_DESTINATION_ADDR] = 1;
                Tx[fld_SENDER_ADDR]      = myEEpromAddress;
                Tx[fld_CMD_RCODE]        = LN_WAITING_FOR_CMD;
                sendMsg232(pData);
                */
            }
            else {
                Serial.print(myID);
                Serial.print(F(" - No data received in the last mS: "));Serial.print(pData->Rx_Timeout);
                Serial.println();
            }
            continue;
        }

            // - echo del comando appena ricevuto
            // - anche se in errore....
        copyRxMessageToTx(pData);
        sendMsg232(pData);

        if (rCode == LN_OK) {

            if (Rx[fld_DESTINATION_ADDR] == myEEpromAddress)  { // facciamo echo del comando....
                processRequest(pData); // esegue come fosse uno slave.
                sendMsg232(pData);
                // fwdToRs232(pData, 0);
            }

            else {
                fwdToRs485(pData);
                    // qualsiasi esito il msg è pronto da inviare sulla rs232
                byte rcvdRCode = Relay_waitRs485Response(pData, 2000);
                copyRxMessageToTx(pData);
                fwdToRs232(pData, rcvdRCode);
            }

        } // end if rcode
    } // end while(true)

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
void fwdToRs232(RXTX_DATA *pData, byte rcvdRCode) {
    // copyRxMessageToTx(pData);

    if (returnRs485ToMaster)
        sendMsg232(pData);
    else
        displayMyData("RX-xxxx", rcvdRCode, pData);

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
byte Relay_waitRs485Response(RXTX_DATA *pData, unsigned long RxTimeout) {


    pData->Rx_Timeout = RxTimeout;
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
        Rx[fld_SENDER_ADDR]      = Rx[fld_DESTINATION_ADDR];
        Rx[fld_DESTINATION_ADDR] = MASTER_ADDRESS;

                      //-- 01234567
        char errorMsg[] = "ERROR: ........ occurred!";
        const char *ptr = errMsg[rcvdRCode];

        // copiamo il codice errore nei [....]
        for (byte i=7; *ptr != '\0'; i++, ptr++)
            errorMsg[i] = *ptr;

        setDataCommand(Rx, errorMsg, sizeof(errorMsg));

    }
    return rcvdRCode;
}