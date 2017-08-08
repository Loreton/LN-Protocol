/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-08_17.03.28

*/


#include <LnFunctions.h>                //  D2X(dest, val, 2)


unsigned char LnFuncWorkingBuff[50];
char workingBuff[10];
void printHex(const byte *data, const byte len, const char *suffixData) {
    byte i;
    for (i=0; i<len; i++) {
        printHex(data[i], " ");
    }
    Serial.print(suffixData);
}

// 2017-03-19 18.29.13 fromt char *workingBuff = "00..."; to char workingBuff[] = "00...";
void printHex(const byte data) {
    // D2X(workingBuff, data, 2);
    // Serial.print(workingBuff);
    char *pippo = (char *) D2XNew(data, 2);
    Serial.print(pippo);
}

void printHex(const byte data, const char *suffixData) {
    D2X(workingBuff, data, 2);
    Serial.print((char *) D2XNew(data, 2));
    Serial.print(suffixData);
}

void printHexPDS(const char *prefixStr, const byte data, const char *suffixStr) {
    Serial.print(prefixStr);
    // D2X(workingBuff, data, 2);
    // D2XNew(LnFuncWorkingBuff, data, 2);
    Serial.print((char *) D2XNew(data, 2));
    Serial.print(suffixStr);
}


void LnPrintStrHex(const char *prefix, byte value, const char *suffix) {
    // D2X(workingBuff, value, 2);
    // D2XNew(LnFuncWorkingBuff, value, 2);
    Serial.print(prefix);
    Serial.print((char *) D2XNew(value, 2));
    Serial.print(suffix);

}



char *LnUtoa(unsigned int i, byte padLen,  byte fill) {
    char *p = &workingBuff[9];
    *p = '\0';                  // chiude il buffer finale

    for(*p--=0; i>0 ;i/=10) {
        *p-- = i%10 + '0';
        padLen--;
        // printf("padLen %i\r\n", padLen);
    }

    // while (padLen--) *p-- = '0';
    while (padLen--) *p-- = fill;

    // printf("%s - %i\r\n", p, padLen);
    return ++p;
}






#if 0
void serialHex_OK(const byte *data, const byte len, char * suffixData) {
    byte i;
    Serial.print("len:");
    Serial.print(len, DEC);
    Serial.print("  -  ");
    char *workingBuff = "0000000000";
    for (i=0; i<len; i++) {
        D2X(workingBuff, data[i], 2);
        Serial.print(workingBuff);
        Serial.print(" ");
    }
    Serial.println(suffixData);
}
#endif