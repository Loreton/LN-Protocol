/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-10_12.29.10

*/


#include <LnFunctions.h>

byte stringLen(const char* data) {
    // - calcolo len
    byte len=0;
    const char *ptr = data;

    while (*ptr++) {len++; }
    return len;
}