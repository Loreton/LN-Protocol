
#include    <EEPROM.h>
#include <LnFunctions.h>



// ################################################################
// # - setMyID
// # char myID[] = "\r\n[Slave-xxx] - "; // i primi due byte sono CR e LF
// ################################################################
char myID[] = "\r\n[YYYYY-xxx] - "; // i primi due byte saranno CR e LF
    extern byte  myEEpromAddress;        // who we are

void setMyID(const char *name) {
    byte i=3;
    byte i1;

    for (i1=0; i1<5; i1++) {
        myID[i++] = name[i1];
    }
    i++; // skip '-'


        // ================================================
        // - Preparazione myID con indirizzo di Arduino
        // -    1. convert integer myAddress to string
        // -    2. copy string into myID array
        // ================================================
    myEEpromAddress = EEPROM.read(0);

    char *xx = Utoa(myEEpromAddress, 3, '0');
    myID[i++] = xx[0];
    myID[i++] = xx[1];
    myID[i++] = xx[2];

    // if (pData->fDisplayMyData) pData->myID = myID;
}
