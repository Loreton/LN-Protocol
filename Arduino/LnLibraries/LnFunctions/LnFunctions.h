// creare il link:
//      cd /usr/share/arduino/libraries
//      sudo ln -s /home/pi/gitREPO/Ln-RS485/ArduinoLibraries/LnFunctions


#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WConstants.h"
#endif


#if not defined(_I_AM_LN_FUNCTIONS_)
    #define _I_AM_LN_FUNCTIONS_

    #define uchar unsigned char

    // #if defined(I_AM_RS485_PROTOCOL_CPP)
    //     #define LN_RCV_ERROR      1
    //     #define LN_RCV_BADCRC     1
    //     #define LN_RCV_BADCHAR    1
    //     #define LN_RCV_TIMEOUT    0
    // #endif

// ARDUINO NANO
// #if defined(_I_AM_ARDUINO_NANO_)  // non funziona - viene ignorato
        #define D00       0         // pin  5
        #define D01       1         // pin  5
        #define D02       2         // pin  5
        #define D03       3         // pin  6
        #define D04       4         // pin  7
        #define D05       5         // pin  8
        #define D06       6         // pin  9
        #define D07       7         // pin 10
        #define D08       8         // pin 11
        #define D09       9         // pin 12
        #define D10      10         // pin 13
        #define D11      11         // pin 14
        #define D12      12         // pin 15
        #define D13      13         // pin 16

        #define A00      A00         // pin 19
        #define A01      A01         // pin 20
        #define A02      A02         // pin 21
        #define A03      A03         // pin 22
        #define A04      A04         // pin 23
        #define A05      A05         // pin 24
        #define A06      A06         // pin 25
        #define A07      A07         // pin 26
// #endif



    void D2X(char * Dest, unsigned int Valore, char size);      // deve essere D2X.cpp

    void printHex(const byte data);
    void printHex(const uchar data,         const char * endStr);
    void printHex(const uchar *data,        const byte len,         const char *endStr="\r\n");
    void printHexPDS(const char *prefixStr, const byte data,        const char *suffixStr="\r\n");

    byte LnCRC8(const byte *data,     byte len);

    void LnPrint(const char *data1, const char *data2="", const char *data3="");
    void LnPrintStrHex(const char *prefix, byte value, const char *suffix="");
    char *LnUtoa(unsigned int i, byte padLen=2, byte fill=' ');

#endif
