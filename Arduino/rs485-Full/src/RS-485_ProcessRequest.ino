/*
Author:     Loreto Notarantonio
version:    LnVer_2017-07-13_07.51.17

Scope:      Process di una richiesta
                Prende i dati dalla rs485, verifica l'indirizzo di destinazione e
                se lo riguarda processa il comando ed invia la risposta.

Ref:        http://www.gammon.com.au/forum/?id=11428
*/




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



// #############################################################
// #
// #############################################################
void sendMessage(byte destAddr, byte data[], byte dataLen, RXTX_DATA *pData) {
    pData->tx[SENDER_ADDR]      = myEEpromAddress;    // SA
    pData->tx[DESTINATION_ADDR] = destAddr;    // DA
    pData->tx[SEQNO_HIGH]       = pData->rx[SEQNO_HIGH];    // riscrivi il seqNO
    pData->tx[SEQNO_LOW]        = pData->rx[SEQNO_LOW];    // DA

    byte index = PAYLOAD;
    for (byte i = 0; i<dataLen; i++)
        pData->tx[index++] = data[i];         // copiamo i dati nel buffer da inviare

    pData->tx[DATALEN] = index;  // set dataLen

        // send to RS-485 bus
    delay(responseDelay);

    digitalWrite(RS485_ENABLE_PIN, ENA_TX);               // enable sending
    sendMsg232(pData);
    digitalWrite(RS485_ENABLE_PIN, ENA_RX);                // set in receive mode
    txDisplayData(0, pData);
}
