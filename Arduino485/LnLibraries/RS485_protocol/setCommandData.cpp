
#include "LnRS485_protocol.h"

// #############################################################
// # Inserisce un messaggio (di errore o altro) nella parte CommandData
// #############################################################
void setCommandData(byte *pData, char cmdData[], byte dataLen) {

        // - calcolo len
    if (dataLen==0) {
        char *ptr = cmdData;
        while (*ptr++) {dataLen++; }
    }


    byte index = fld_COMMAND_DATA-1;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData[++index] = cmdData[i];         // copiamo i dati nel buffer da inviare

    pData[fld_DATALEN] = --index;  // update dataLen
}