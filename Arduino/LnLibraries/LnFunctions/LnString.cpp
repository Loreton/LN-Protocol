/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-08_16.45.59

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)


// void joinString(char *returnBuffer, const char *s1, const char *s2, const char *s3, const char *s4 ) {
int joinString(unsigned char *returnBuffer, const char *s1, const char *s2, const char *s3, const char *s4) {
    unsigned char *ptr = returnBuffer;
    const char *str;
    int len = 0;

    str =  s1;
    while (*str) {*ptr++ = *str++; len++; }

    str = s2;
    while (*str) {*ptr++ = *str++; len++; }

    str = s3;
    while (*str) {*ptr++ = *str++; len++; }

    str = s4;
    while (*str) {*ptr++ = *str++; len++; }

    *ptr ='\0'; //fine stringa
    return len;

}



char *LnUtoa2(unsigned int i, byte padLen,  byte fill) {
    unsigned char *p = &LnFuncWorkingBuff[9];
    *p = '\0';                  // chiude il buffer finale

    for(*p--=0; i>0 ;i/=10) {
        *p-- = i%10 + '0';
        padLen--;
        // printf("padLen %i\r\n", padLen);
    }

    // while (padLen--) *p-- = '0';
    while (padLen--) *p-- = fill;

    // printf("%s - %i\r\n", p, padLen);
    return (char*) ++p;
}



