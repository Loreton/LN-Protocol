
#include "LnRS485_protocol.h"

// ################################################################
// # - Copia l'intero messaggio
// # -  RxBuffer --> TxBuffer
// ################################################################
void copyRxMessageToTx(RXTX_DATA *pData) {
        // - copy ALL rx to tx
    for (byte i = 0; i<=pData->rx[fld_DATALEN]; i++)
        pData->tx[i] = pData->rx[i];         // copiamo i dati nel buffer da inviare

    // inverti end point partners address
    // pData->tx[SENDER_ADDR]      = pData->rx[DESTINATION_ADDR];
    // pData->tx[DESTINATION_ADDR] = pData->rx[SENDER_ADDR];
}