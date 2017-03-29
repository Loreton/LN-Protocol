
#include <LnFunctions.h>                //  D2X(dest, val, 2)
// char * rvcvdByte = "0";
// void printChar(byte data, cha);
void printHex(const byte *data, const byte len, const char *suffixData) {
    byte i;
    for (i=0; i<len; i++) {
        printHex(data[i], " ");
    }
    Serial.print(suffixData);
}

// 2017-03-19 18.29.13 fromt char *strBuff = "00..."; to char strBuff[] = "00...";
char strBuff[] = "00...";      // notare il BLANK come ultimo carattere. Separa i vari bytes
void printHex(const byte data) {
    D2X(strBuff, data, 2);
    Serial.print(strBuff);
}

void printHex(const byte data, const char *suffixData) {
    D2X(strBuff, data, 2);
    Serial.print(strBuff);
    Serial.print(suffixData);
}

void printHexPDS(const char *prefixStr, const byte data, const char *suffixStr) {
    Serial.print(prefixStr);
    D2X(strBuff, data, 2);
    Serial.print(strBuff);
    Serial.print(suffixStr);
}


void LnPrintStrHex(const char *prefix, byte value, const char *suffix) {
    D2X(strBuff, value, 2);
    Serial.print(prefix);
    Serial.print(strBuff);
    Serial.print(suffix);

}




#if 0
void serialHex_OK(const byte *data, const byte len, char * suffixData) {
    byte i;
    Serial.print("len:");
    Serial.print(len, DEC);
    Serial.print("  -  ");
    char *strBuff = "0000000000";
    for (i=0; i<len; i++) {
        D2X(strBuff, data[i], 2);
        Serial.print(strBuff);
        Serial.print(" ");
    }
    Serial.println(suffixData);
}
#endif