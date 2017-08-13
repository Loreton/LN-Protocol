// creare il link:
//      cd /usr/share/arduino/libraries
//      sudo ln -s /home/pi/gitREPO/Ln-RS485/ArduinoLibraries/LnFunctions


#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WConstants.h"
#endif

// byte  myEEpromAddress;        // who we are
#if not defined(_I_AM_LN_FUNCTIONS_)
    #define _I_AM_LN_FUNCTIONS_

    #define uchar unsigned char

    extern unsigned char LnFuncWorkingBuff[]; // 50 bytes
    extern char sharedWorkingBuff[]; // 50 bytes
    extern char myID[];


    char *D2X(unsigned int Valore, char size);      // deve essere D2X.cpp
    void printHex(const byte data);
    void printHex(const char *data,     byte len=0,  const char *suffixData="", const char *sep=" ");
    void printHexPDS(const char *prefixStr, const byte data,        const char *suffixStr="\n");


    void printNchar(const char data, byte counter); // print un byte N volte

    void printDelimitedStr(const char *data, byte len=0, const char *delimiter=NULL);  // print di una stringa visibile

    char *Utoa(unsigned int i, byte padLen=2, byte fill=' ');
    char *joinStr(const char *fmt, ...);
    byte stringLen(const char* data);
    void setMyID(const char *name);
    // char *getMyID(void);




    #if defined(_I_AM_ARDUINO_NANO_)
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
    #endif


#endif
