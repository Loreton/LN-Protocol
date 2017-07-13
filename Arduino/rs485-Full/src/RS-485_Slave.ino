/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-13_07.56.06

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
    pData->timeout  = 10000;
    byte rCode      = recvMsg485(pData);

    if (rCode == LN_OK) {
        processRequest(pData);
        Serial232.println();
    }

    else if (pData->rx[DATALEN] == 0) {
        Serial232.print(myID);
        Serial232.print(F("rCode: "));Serial232.print(rCode);
        Serial232.print(F(" - Nessuna richiesta ricevuta in un tempo di mS: "));
        Serial232.print(pData->timeout);
        Serial232.println();
    }

    else {
        rxDisplayData(rCode, pData);
        Serial232.println();
    }

}
