/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-16_11.59.01

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)

// print di ogni carattere di una stringa
// convertito in HEX e con il separatore indicato
// void printHex(const byte *data, const byte len=0, const char *suffixData="", const char *sep=" ");
void printHex(const char *data, byte len, const char *suffixData, const char *sep) {
    byte i;

    if (len==0) len = stringLen(data);

    for (i=0; i<len; i++) {
        Serial.print(D2X(data[i], 2));
        Serial.print(sep);
    }
    Serial.print(suffixData);
}

// print di ogni carattere di una stringa
// convertito in HEX e con il separatore indicato
void printDataToHex(const char *data, byte len, const char *sep) {
    byte i;
    for (i=0; i<len; i++) {
        Serial.print(D2X(data[i], 2));
        if ( (len-i) > 1 )
            Serial.print(sep);
    }

}


void printHex(const byte data) {
    Serial.print(D2X(data, 2));
}



void printHexPDS(const char *prefixStr, const byte data, const char *suffixStr) {
    Serial.print(prefixStr);
    Serial.print(D2X(data, 2));
    Serial.print(suffixStr);
}

