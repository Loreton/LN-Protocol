/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-09_16.01.07

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)


// void joinString(char *returnBuffer, const char *s1, const char *s2, const char *s3, const char *s4 ) {
int joinStr(unsigned char *returnBuffer, const char *s1, const char *s2, const char *s3, const char *s4) {
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

