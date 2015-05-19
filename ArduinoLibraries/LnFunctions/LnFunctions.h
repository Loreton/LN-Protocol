// creare il link:
//      cd /usr/share/arduino/libraries
//      sudo ln -s /home/pi/gitREPO/Ln-RS485/ArduinoLibraries/LnFunctions


#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WConstants.h"
#endif


#if defined(I_AM_LN_FUNCTIONS)

    // SET_CRC_BEFORE_ETX = true;    // by Loreto

#else
    #define I_AM_LN_FUNCTIONS
    #define uchar unsigned char

    #define RCV_ERROR      1
    #define RCV_BADCRC     1
    #define RCV_BADCHAR    1
    #define RCV_TIMEOUT    0


    // bool  SET_CRC_BEFORE_ETX = false;    // by Loreto
    // bool  SET_CRC_BEFORE_ETX = true;    // by Loreto


    void D2X(char * Dest, unsigned int Valore, char size);      // deve essere D2X.cpp

    void printHex(uchar data,               const char * endStr);
    void printHex(const uchar *data,        const byte len,     const char * endStr);
    // void printHex(const byte * prefixLine,  byte data,          const char * suffixLine);
    // void printHex(const byte * prefixLine,  const byte *data,   const byte len, const char * suffixLine);
#endif
