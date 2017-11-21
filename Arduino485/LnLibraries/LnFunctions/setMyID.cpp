
#define I_AM_SET_MY_ID_
#include <LnFunctions.h>



void setMyID(const char *name, byte myEEpromAddress) {
    byte i=3;
    byte i1;

    for (i1=0; i1<5; i1++) {
        myID[i++] = name[i1];
    }
    i++; // skip '-'

    char *xx = Utoa(myEEpromAddress, 3, '0');
    myID[i++] = xx[0];
    myID[i++] = xx[1];
    myID[i++] = xx[2];

}
