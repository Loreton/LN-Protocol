// creare il link:
//      cd /usr/share/arduino/libraries
//      sudo ln -s /home/pi/gitREPO/Ln-RS485/ArduinoLibraries/LnFunctions


#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WConstants.h"
#endif






#if defined (I_AM_SET_MY_ID_)
    char myID[] = "\r\n[YYYYY-xxx] - "; // i primi due byte saranno CR e LF
#else
    extern char  myID[];
#endif



        // http://www.keywild.com/arduino/gallery/Nano_PinOut.png
#if defined(_I_AM_ARDUINO_NANO_)
        #define D00       0         // pin.30 D00 - RS232:RXD
        #define D01       1         // pin.31 D01 - RS232:TXD

        #define D02       2         // pin.32 - D02 -           -
        #define D03       3         // pin.01 - D03 -           - PWM
        #define D04       4         // pin.02 - D04 - I2C:SDA
        #define D05       5         // pin.09 - D05 - I2C:SCL   - PWM
        #define D06       6         // pin.10 - D06 -           - PWM
        #define D07       7         // pin.11 - D07 -           -
        #define D08       8         // pin.12 - D08 -           -
        #define D09       9         // pin.13 - D09 -           - PWM
        #define D10      10         // pin.14 - D10 - SPI:SS    - PWM
        #define D11      11         // pin.15 - D11 - SPI:MOSI  - PWM
        #define D12      12         // pin.16 - D12 - SPI:MISO  -
        #define D13      13         // pin.17 - D13 - SCK       - R1K + LED

        #define A00      A00        // pin.19 - A00-D14 - Analog or Digital
        #define A01      A01        // pin.20 - A01-D15 - Analog or Digital
        #define A02      A02        // pin.21 - A02-D16 - Analog or Digital
        #define A03      A03        // pin.22 - A03-D17 - Analog or Digital
        #define A04      A04        // pin.23 - A04-D18 - Analog or Digital
        #define A05      A05        // pin.24 - A05-D19 - Analog or Digital

        #define A06      A06        // pin.25 - A06         - Analog exclusive pins
        #define A07      A07        // pin.26 - A06         - Analog exclusive pins
#endif

#if not defined(_I_AM_LN_FUNCTIONS_)
    #define _I_AM_LN_FUNCTIONS_

    #define uchar unsigned char

#endif



// ----------- F U N C T I O N S  -------------------


    extern unsigned char LnFuncWorkingBuff[]; // 50 bytes
    extern char sharedWorkingBuff[]; // 50 bytes


    char *D2X(unsigned int Valore, char size);      // deve essere D2X.cpp
    void printHex(const byte data);
    void printHex(const char *data,  byte len=0,  const char *suffixData="", const char *sep=" ");
    void printHexPDS(const char *prefixStr, const byte data,        const char *suffixStr="\n");
    void printDataToHex(const char *data, byte len, const char *sep);


    void printNchar(const char data, byte counter); // print un byte N volte

    void printDelimitedStr(const char *data, byte len=0, const char *delimiter=NULL);  // print di una stringa visibile

    char *Utoa(unsigned int i, byte padLen=2, byte fill=' ');
    char *joinStr(const char *fmt, ...);
    byte stringLen(const char* data);
    void setMyID(const char *name, byte myEEpromAddress);

    void print6Str(const char *s1, const char *s2="", const char *s3="", const char *s4="", const char *s5="", const char *s6="");


    void printPINs(void);