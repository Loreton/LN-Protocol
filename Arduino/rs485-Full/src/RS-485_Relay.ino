/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-13_08.29.44

Scope:      Funzione di relay.
                Prende i dati provenienti da una seriale collegata a RaspBerry
                ed inoltra il comando sul bus RS485.
                Provvede ovviamente a catturare la risposta e reinoltrarla a RaspBerry.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/




// ################################################################
// # - M A I N     Loop_Relay
// #    - riceviamo i dati da RaspBerry
// #    - facciamo il forward verso rs485
// #    - torniamo indietro la risposta
// ################################################################
void loop_Relay() {
    pData->timeout     = 5000;
    pData->rx[DATALEN] = 0;
    byte rCode         = recvMsg232(pData);

    if (rCode == LN_OK) {
        forwardMessage(pData);
    }
}




// ################################################################
// # - Copia l'intero messaggio presente nel RxBuffer
// # -   nel TxBuffer
// # -   nel bus485 cambiando il solo SourceAddress
// ################################################################
void forwardMessage(RXTX_DATA *pData) {
    byte dataLen = pData->rx[DATALEN];

        // - copy ALL rx to tx
    for (byte i = 0; i<=dataLen; i++)
        pData->tx[i] = pData->rx[i];         // copiamo i dati nel buffer da inviare

    // imposta sender address (Arduino Relay)
    pData->tx[DESTINATION_ADDR] = pData->rx[SENDER_ADDR];
    pData->tx[SENDER_ADDR]      = myEEpromAddress;

        // invia il messaggio indietro a raspBerry
        // per far capire che è presente ed ha capito
    if (pData->rx[COMMAND] == ECHO_CMD) {
        sendMsg232(pData);
    }

        // send to RS-485 bus
    digitalWrite(RS485_ENABLE_PIN, ENA_485_TX);               // enable Rs485 sending
    sendMsg485(pData);
    digitalWrite(RS485_ENABLE_PIN, ENA_485_RX);               // set in receive mode

}


