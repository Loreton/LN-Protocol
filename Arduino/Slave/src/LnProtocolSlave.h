#if 1
__asm volatile ("nop");
#endif
// #include <Arduino.h>

//Include the VirtualWire library
#define DR3100x                         // altro tipo di trasmitter
#include <VirtualWire.h>                // RX-Default D11  TX-Default D12 TX_Enable_pin D10

#define _I_AM_ARDUINO_NANO_
#include <LnFunctions.h>                // D2X(dest, val, 2), printHex()
#include <LnProtocol.h>                // definizioni di STX etc..


#if defined(_I_AM_MAIN_)
    #define EXTERNAL_TYPE

#else
    #define EXTERNAL_TYPE extern

#endif


    void readDigitalPin(byte a, byte b);
