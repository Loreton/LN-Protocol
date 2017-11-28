/*
per compilare c++ online:
    https://www.codechef.com/ide
    https://www.tutorialspoint.com/compile_cpp_online.php   -- anche python

version : LnVer_2017-08-10_12.29.10

*/


#include <LnFunctions.h>

void printPINs() {
    const char TAB4[] = "\n    ";
    // Serial.print(TAB4);Serial.print(F("Digital D0 - 0x:"));printHex(A0);Serial.print(" dec:");Serial.print(D0);
    Serial.println(F(""));
    Serial.print(TAB4);Serial.print(F("Analog  A0 - 0x:"));printHex(A0);Serial.print(" dec:");Serial.print(A0);
    Serial.print(TAB4);Serial.print(F("Analog  A1 - 0x:"));printHex(A1);Serial.print(" dec:");Serial.print(A1);
    Serial.print(TAB4);Serial.print(F("Analog  A2 - 0x:"));printHex(A2);Serial.print(" dec:");Serial.print(A2);
    Serial.print(TAB4);Serial.print(F("Analog  A3 - 0x:"));printHex(A3);Serial.print(" dec:");Serial.print(A3);
    Serial.print(TAB4);Serial.print(F("Analog  A4 - 0x:"));printHex(A4);Serial.print(" dec:");Serial.print(A4);
    Serial.print(TAB4);Serial.print(F("Analog  A5 - 0x:"));printHex(A5);Serial.print(" dec:");Serial.print(A5);
    Serial.print(TAB4);Serial.print(F("Analog  A6 - 0x:"));printHex(A6);Serial.print(" dec:");Serial.print(A6);
    Serial.print(TAB4);Serial.print(F("Analog  A7 - 0x:"));printHex(A7);Serial.print(" dec:");Serial.print(A7);
    Serial.println(F(""));
    delay(5000);
}