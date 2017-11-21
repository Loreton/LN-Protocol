/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-10_10.29.01

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)

char UtoaBuffer[10];  // buffer dedicato
char *Utoa(unsigned int i, byte padLen,  byte fill) {
    char *ptr = &UtoaBuffer[9];
    *ptr = '\0';                  // chiude il buffer finale

    for(*ptr--=0; i>0 ;i/=10) {
        *ptr-- = i%10 + '0';
        padLen--;
    }

    while (padLen--) *ptr-- = fill;
    return ++ptr;
}

