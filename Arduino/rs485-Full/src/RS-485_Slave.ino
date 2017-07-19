/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-19_18.34.04

Scope:      Funzione di slave.
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/


// ################################################################
// # - M A I N     Loopslave
// #    - riceviamo i dati da rs485
// #    - elaboriamo il comando ricevuto
// #    - rispondiamo se siamo interessati
// ################################################################
void loop_Slave() {
    pData->displayData  = false;                // data display dei byte hex inviati e ricevuti
    pData->timeout      = 10000;

    byte rCode      = recvMsg485(pData);

    if (rCode == LN_OK) {
        processRequest(pData);
        Serial232.println();
    }

        // lo slave scrive sulla seriale come debug
    else if (pData->rx[DATALEN] == 0) {
        Serial232.print(myID);
        Serial232.print(F("rCode: "));Serial232.print(rCode);
        Serial232.print(F(" - Nessuna richiesta ricevuta in un tempo di mS: "));
        Serial232.print(pData->timeout);
        Serial232.println();
    }

    else { // DEBUG
        rxDisplayData(rCode, pData);
        Serial232.println();
    }

}




// #############################################################
// #
// #############################################################
void processRequest(RXTX_DATA *pData) {
    byte senderAddr = pData->rx[SENDER_ADDR];
    byte destAddr   = pData->rx[DESTINATION_ADDR];
    int seqNO       = pData->rx[SEQNO_HIGH]*256 + pData->rx[SEQNO_LOW];

    Serial232.print(myID);  Serial232.print(F("inoRECV from: ")); Serial232.print(senderAddr);
                            Serial232.print(F(" to  : ")); Serial232.print(destAddr);
                            Serial232.print(F(" [")); Serial232.print(LnUtoa(seqNO,5,'0'));Serial232.print(F("]"));

    if (destAddr == myEEpromAddress) {    // sono io.... rispondi sulla RS485
        Serial232.print(F("   (Request is for me) ... answering"));
        sendMsg232(pData);
    }
    else {                                // non sono io.... commento sulla seriale
        Serial232.print(F("   (Request is NOT for me)"));
        rxDisplayData(0, pData);
    }
}
