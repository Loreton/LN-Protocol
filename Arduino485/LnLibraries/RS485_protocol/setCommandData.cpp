
#include "LnRS485_protocol.h"

// #############################################################
// # Inserisce un messaggio (di errore o altro) nella parte CommandData
// #############################################################
void setDataCommand(byte *pData, char cmdData[], byte dataLen) {

    byte index = fld_DATA_COMMAND;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData[index++] = cmdData[i];         // copiamo i dati nel buffer da inviare

    pData[fld_DATALEN] = --index;  // update dataLen
}


