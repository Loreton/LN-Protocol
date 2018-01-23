/*
Author:     Loreto Notarantonio

# updated by ...: Loreto Notarantonio
# Version ......: 23-01-2018 10.25.36


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
    RxTimeout = 100000;         // set timeout
    pData->Rx_Timeout = RxTimeout;         // set timeout
    I_AM_RELAY  = true;
    I_AM_SLAVE  = false;


    while (true) {
        // Serial.print(myID); Serial.print(F(" sono qui: 00"));Serial.println();

        Rx[fld_DATALEN]   = 0;

            // -------------------------------------------
            // - ricezione messaggio da RaspBerry (Rs232)
            // -------------------------------------------
        byte rCode = recvMsg232(pData);
        // Serial.print(myID); Serial.print(F(" - rcode: "));Serial.print(rCode);Serial.println(errMsg[rCode]);

        // rCode = LN_OK;

        if (rCode == LN_TIMEOUT) {
            if (returnRs485ToMaster == true) {
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
        // displayRXFull(pData);

            /*
                echo del comando appena ricevuto
                come ack verso RaspBerry
            */

        copyRxMessageToTx(pData);
        sendMsg232(pData);

        if (rCode == LN_OK) {
            // Serial.print(myID); Serial.print(F(" sono in RC=OK"));Serial.println();

                // processiamo il comando come fossimo uno slave.
            if (Rx[fld_DESTINATION_ADDR] == myEEpromAddress)  {
                Serial.print(myID); Serial.print(F(" sono in LOCAL Execution"));Serial.println();
                // processRequest(pData);
            }

            else {
                // Serial.print(myID); Serial.print(F(" sono in FWD"));Serial.println();
                    // forward message to Rs485 bus
                Relay_fwdToRs485(pData);
                    // wait for response
                byte rcvdRCode = Relay_waitRs485Response(pData, 2000);
                    // forward message to RaspBerry (rs232)
                Relay_fwdToRaspBerry(pData, rcvdRCode);
            }
        }

        // Serial.print(myID); Serial.print(F(" sono qui: 03"));Serial.println();
    } // end while true
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

    if (returnRs485ToMaster == true)
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

#if 0
void displayRXFull(RXTX_DATA *pData) {
    const byte *data;
    const byte *raw;
    byte  rawIndex=0;

    raw = pData->raw;
    data = pData->rx;
    // byte dataLen = data[fld_DATALEN];
    byte rawLen  = raw[0];

    if (rawLen > 0) {
        rawIndex = fld_DATA_COMMAND*2;
        Serial.println();
        Serial.print(TAB4);Serial.print(F("full raw - len:["));Serial.print(Utoa(raw[0], 3, '0'));Serial.print(F("] - "));
        Serial.print(TAB4);printHex((char *) &raw[1], raw[0]); //Serial.println();

        Serial.println();
        Serial.print(TAB4);Serial.print(F("CMD  raw -      "));;Serial.print(Utoa(raw[0], 3, '0'));
        Serial.print(TAB4);printHex((char *) &raw[rawIndex], rawLen-rawIndex-2);//Serial.println();

    }
}
#endif