/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-09_15.52.59

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)

unsigned char *LnUtoa(unsigned int i, byte padLen,  byte fill) {
    unsigned char *ptr = &LnFuncWorkingBuff[9];
    *ptr = '\0';                  // chiude il buffer finale

    for(*ptr--=0; i>0 ;i/=10) {
        *ptr-- = i%10 + '0';
        padLen--;
    }

    while (padLen--) *ptr-- = fill;
    return ++ptr;
}

