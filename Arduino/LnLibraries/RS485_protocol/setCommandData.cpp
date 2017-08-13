
#include "LnRS485_protocol.h"
// #include <LnFunctions.h>        // stringLen

// #############################################################
// # Inserisce un messaggio (di errore o altro) nella parte CommandData
// #############################################################
void setCommandData(byte *pData, char cmdData[], byte dataLen) {
    if (dataLen==0) {
        // - calcolo len
        // byte len=0;
        char *ptr = cmdData;

        while (*ptr++) {dataLen++; }
        // return len;
        // dataLen = stringLen(cmdData);
    }


    byte index = COMMAND_DATA-1;
    for (byte i=0; (i<dataLen) && (i<MAX_DATA_SIZE); i++)
        pData[++index] = cmdData[i];         // copiamo i dati nel buffer da inviare

    pData[DATALEN] = --index;  // update dataLen
    // displayMyData(INO_Prefix,  LN_OK, pData);
}